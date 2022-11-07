from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesListView, CommentViewSet, GenreListView,
                    ReviewViewSet, TitleListView, UserViewSet,
                    RegisterUserAPIView, ObtainTokenView)


api_v1_router = DefaultRouter()
api_v1_router.register('users', UserViewSet)
api_v1_router.register('titles', TitleListView)
api_v1_router.register('genres', GenreListView)
api_v1_router.register('categories', CategoriesListView)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('token/', ObtainTokenView.as_view(), name='token'),
]

urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
    # Authorization
    path('v1/auth/', include(auth_urls)),
]
