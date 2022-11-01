
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from .permissions import OwnerOrAdminOnly, SelfPermission
from .serializers import UserSerializer, RegisterSerializer, GetTokenSerializer

from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (OwnerOrAdminOnly,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    @action(methods=['GET', 'PATCH'], detail=False, permission_classes=[SelfPermission],
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
