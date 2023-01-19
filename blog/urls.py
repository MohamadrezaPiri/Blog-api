from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet, PostImageViewSet


router = routers.SimpleRouter()

router.register('posts', PostViewSet, basename='post')

posts_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')
posts_router.register('images', PostImageViewSet, basename='post-images')

urlpatterns = router.urls + posts_router.urls
