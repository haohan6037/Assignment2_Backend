from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Post, Like  # 假设你有一个 Like 模型来记录点赞
from rest_framework.authtoken.models import Token

class LikePostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.post = Post.objects.create(title='Test Post', content='Content here', author=self.user)
        self.like_url = f'/api/posts/{self.post.id}/like/'

    def test_like_post_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.like_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data['liked'])
        self.assertEqual(response.data['liked'], True)
        self.assertEqual(response.data['like_count'], 1)