from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, data):
        if data == 'me':
            raise serializers.ValidationError(
                'This username is not allowed!')
        return data


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=5)

    def validate(self, data):
        try:
            user = User.objects.get(username=data.get('username'))
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f'User <{data.get("username")}> does not exist.'
            )
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Confirmation code is incorrect.')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'This username is not allowed!')
        return data
