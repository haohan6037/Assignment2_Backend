from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.models import Post
from api.serializers import PostSerializer


class PostListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='SecurePass123')
        self.post1 = Post.objects.create(
            title="Post 1",
            content="Content 1",
            category="Tech",
            author=self.user
        )
        self.post2 = Post.objects.create(
            title="Post 2",
            content="Content 2",
            category="Life",
            author=self.user
        )
        self.url = reverse('post-list')

    def test_post_list_view_returns_all_posts(self):
        print("Unit test post list start")
        response = self.client.get(self.url)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        print("Unit test post list pass")

