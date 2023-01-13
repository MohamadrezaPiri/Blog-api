from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'title', 'content']

    user_id = serializers.IntegerField(read_only=True)

    def save(self):
        user_id = self.context['user_id']
        title = self.validated_data['title']
        content = self.validated_data['content']
        Post.objects.create(user_id=user_id, title=title, content=content)


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']
