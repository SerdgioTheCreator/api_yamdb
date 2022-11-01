from django.core.mail import send_mail
from rest_framework.exceptions import NotFound
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='This username is already taken.'
        )]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='This email is already being used by another user.'
        )]
    )
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'This username is not allowed!')
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            confirmation_code=get_random_string(length=5)
        )
        user.save()
        send_mail(
            'Confirmation code',
            f'Here is your code: {user.confirmation_code}.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        return user


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=5)
    
    def validate(self, data):
        try:
            user = User.objects.get(username=data.get('username'))
        except:
            raise NotFound(detail=f'User <{data.get("username")}> does not exist.')
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Confirmation code is incorrect.')
        return data

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']
    
    
