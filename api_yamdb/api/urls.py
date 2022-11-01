from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesListView, CommentViewSet, GenreListView, TitleListView

api_v1_router = DefaultRouter()
api_v1_router.register('titles', TitleListView)
api_v1_router.register('genres', GenreListView)
api_v1_router.register('categories', CategoriesListView)
api_v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                       CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(api_v1_router.urls)),
]
