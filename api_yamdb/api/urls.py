from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesListView, CommentViewSet, GenreListView,
                    ReviewViewSet, TitleListView)


api_v1_router = DefaultRouter()
api_v1_router.register('titles', TitleListView, basename='titles')
api_v1_router.register('genres', GenreListView, basename='genres')
api_v1_router.register('categories', CategoriesListView, basename='categories')
api_v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                       ReviewViewSet, basename='reviews')
api_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
]
