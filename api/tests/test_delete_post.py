from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Post
from django.urls import reverse

class DeletePostViewTest(APITestCase):
    def setUp(self):
        # create user
        self.user1 = User.objects.create_user(username='user5', password='123456')
        self.token_url = '/api/token-auth/'
        # user1 create post
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user1, category='Tech')
        # delete url
        self.delete_url = reverse('delete-post', kwargs={'pk': self.post.pk})


    def authenticate(self):
        response = self.client.post(
            self.token_url,
            data={"username": "user5", "password": "123456"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    def test_delete_own_post_authenticated(self):
        self.authenticate()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())