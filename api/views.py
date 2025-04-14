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
            return JsonResponse({'token': token.key}, status=201)



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