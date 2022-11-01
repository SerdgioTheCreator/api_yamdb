from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterUserAPIView, ObtainTokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', RegisterUserAPIView.as_view(), name='signup'),
    path('v1/auth/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('v1/', include(router_v1.urls)),
]