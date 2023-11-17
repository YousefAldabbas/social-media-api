from rest_framework import routers

from social_media.views import CategoryViewSet, PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)
router.register("category", CategoryViewSet)


urlpatterns = router.urls

app_name = "social_media"
