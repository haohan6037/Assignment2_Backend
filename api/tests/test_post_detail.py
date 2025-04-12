from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Post

class PostDetailTestCase(APITestCase):
    def setUp(self):
        # Create a user and a known post with ID = 1
        self.user = User.objects.create_user(username='testuser', password='SecurePass123')
        self.post = Post.objects.create(
            id=1,  # Ensure ID is 1 for consistency
            title='Test Post',
            content='This is the detail of test post.',
            category='Tech',
            author=self.user
        )

    def test_get_post_detail_by_id_1(self):
        response = self.client.get('/api/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], 'Test Post')
        print("post detail unit testing pass!! post id = 1 title = Test Post ="+response.data['title'])
