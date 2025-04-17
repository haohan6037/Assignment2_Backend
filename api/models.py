from django.db import models

from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Tech', 'Tech'),
        ('Life', 'Life'),
        ('Study', 'Study'),
        ('Travel', 'Travel'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # 限制每个用户只能对一个帖子点赞一次

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"