from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import Post, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'description', 'date']

    def save(self):
        user_id = self.context['user_id']
        post_id = self.context['post_id']
        description = self.validated_data['description']
        Comment.objects.create(
            user_id=user_id, post_id=post_id, description=description)


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description']
