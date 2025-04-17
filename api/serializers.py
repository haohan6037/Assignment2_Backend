from rest_framework import serializers

from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'created_at', 'updated_at', 'author', 'like_count', 'liked_by_user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(user=user).exists() if user.is_authenticated else False
