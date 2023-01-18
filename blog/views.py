from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, UpdatePostSerializer, CommentSerializer, UpdateCommentSerializer
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdatePostSerializer
        else:
            return PostSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateCommentSerializer
        else:
            return CommentSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'post_id': self.kwargs['post_pk']}
