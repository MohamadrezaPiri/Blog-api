from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer, UpdatePostSerializer
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return UpdatePostSerializer
        else:
            return PostSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
