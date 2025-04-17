from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import Post
from api.serializers import PostSerializer


# Create your views here.


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username = data['username'], password = data['password'])
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({'token': token.key}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'username already exists'}, status=400)



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])

        if user is None:
            return JsonResponse({'error': 'invalid credentials'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': token.key, 'username': user.username, 'id': user.id}, status=201)


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        # 检查认证头
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Missing or invalid Authorization header'}, status=401)

        # 提取 Token
        token_key = auth_header.split(' ')[1].strip()
        if not token_key:
            return JsonResponse({'error': 'Invalid token format'}, status=401)

        try:
            # 删除 Token
            token = Token.objects.get(key=token_key)
            # token.delete()
            return JsonResponse({'message': 'Successfully logged out'}, status=200)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


class CreatePostView(generics.CreateAPIView):
    print("CreatePostView")
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    print("CreatePostView permission_classes:", permissions.IsAuthenticated)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



# Get a single post by ID
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        print("DeletePostView: user=", request.user)
        return self.destroy(request, *args, **kwargs)
