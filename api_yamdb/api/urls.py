from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import TitleListView, GenryListView, CategoriesListView

router_v1 = DefaultRouter()
router_v1.register('titles', TitleListView)
router_v1.register('genrys', GenryListView)
router_v1.register('categories', CategoriesListView)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
