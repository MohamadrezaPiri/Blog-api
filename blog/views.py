from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework.backends import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment, PostImage
from .serializers import PostSerializer, UpdatePostSerializer, CommentSerializer, UpdateCommentSerializer, PostImageSerializer
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related('images').all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = PageNumberPagination
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
        comment = Comment.objects.filter(post_id=self.kwargs['post_pk'])
        if comment.exists():
            return comment
        else:
            raise NotFound('There is no post or comment with the given ID')

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdateCommentSerializer
        else:
            return CommentSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'post_id': self.kwargs['post_pk']}


class PostImageViewSet(ModelViewSet):

    serializer_class = PostImageSerializer

    def get_queryset(self):
        return PostImage.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'post_id': self.kwargs['post_pk']}
