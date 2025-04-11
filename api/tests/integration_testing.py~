import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from api.models import Post


class IntegrationTests(TestCase):
    # register testing
    def test_successful_registration(self):
        data = {'username': 'testuser', 'password': 'SecurePass123'}
        signup_response = self.client.post(
            reverse('signup'),
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(signup_response.status_code, 201)
        token = signup_response.json().get('token')
        self.assertIsNotNone(token)
        print("1 register testing pass!!")

        # get token
        self.token=token

        # create post
        post_data = {
            "title": "My First Integration Post",
            "content": "This post is part of an integration test.",
            "category": "Tech"
        }

        response = self.client.post('/api/posts/create/', data=post_data, format='json', HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, post_data['title'])
        print("2 create post testing pass!!")

