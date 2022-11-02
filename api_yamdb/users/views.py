from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminOrMyselfOnly
from .serializers import GetTokenSerializer, RegisterSerializer, UserSerializer
from .utils import create_and_send_code


class UserViewSet(viewsets.ModelViewSet):
    '''Viewset for User endpoints with 'me' endpoint included.'''
    queryset = User.objects.all()
    permission_classes = [AdminOrMyselfOnly]
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me',
        url_name='me'
    )
    def retrieve_patch_me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    '''Viewset for User registration.'''
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        username = request.data.get('username')
        if not User.objects.filter(username=username).exists():
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            create_and_send_code(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = get_object_or_404(User, username=username)
        serializer = RegisterSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['email'] == user.email:
            serializer.save()
            create_and_send_code(username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {'error': 'This email is already being used by another user.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ObtainTokenView(APIView):
    '''Viewset for User to get authorization token.'''
    permission_classes = [AllowAny]
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(username=serializer.validated_data['username'])
        refresh = RefreshToken.for_user(user)
        token = {'token': str(refresh.access_token)}
        return Response(token, status=status.HTTP_200_OK)
