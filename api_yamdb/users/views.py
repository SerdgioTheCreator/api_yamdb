
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .permissions import OwnerOrAdminOnly
from .serializers import UserSerializer, RegisterSerializer, GetTokenSerializer

from .models import User


def conf_code_send(email):
    code = get_random_string(length=5)
    send_mail(
            'Confirmation code',
            f'Here is your code: {code}.',
            'from@example.com',
            [f'{email}'],
            fail_silently=False,
        )
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (OwnerOrAdminOnly,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    @action(methods=['GET', 'PATCH'], detail=False, permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
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

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data.confirmation_code=conf_code_send(response.data.get("email"))
        # send_mail(
        #     'Confirmation code',
        #     f'Here is your code: {response.data.confirmation_code}.',
        #     'from@example.com',
        #     [f'{response.data.get("email")}'],
        #     fail_silently=False,
        # )
        return Response(response.data, status=status.HTTP_200_OK)

        
class ObtainTokenView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer
    
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.get(username=serializer.validated_data['username'])
        refresh = RefreshToken.for_user(user)
        token = {'token': str(refresh.access_token)}
        return Response(token, status=status.HTTP_200_OK)
