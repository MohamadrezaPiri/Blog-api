# from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet


router = routers.SimpleRouter()

router.register('posts', PostViewSet, basename='post')

posts_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls + posts_router.urls
