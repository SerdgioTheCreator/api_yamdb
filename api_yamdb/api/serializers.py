from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueTogetherValidator

from .validators import UsernameValidator
from api_yamdb.settings import (AUTH_USERNAME_MAXLENGTH,
                                AUTH_EMAIL_MAXLENGTH,
                                AUTH_CONF_CODE_MAXLENGTH)
from reviews.models import Categories, Comment, Genre, Review, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(
        read_only=True
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleDefault:
    requires_context = True

    def __call__(self, data):
        return get_object_or_404(
            Title,
            id=data.context['view'].kwargs.get('title_id')
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=TitleDefault())

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]

    # def validate_score(self, score):
    #     if not 1 <= score <= 10:
    #         raise serializers.ValidationError(
    #             'Score should be set in the range from 1 to 10.')
    #     return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=AUTH_USERNAME_MAXLENGTH,
        required=True,
        validators=(UsernameValidator(),)
    )


class RegisterSerializer(AuthSerializer):
    email = serializers.EmailField(
        max_length=AUTH_EMAIL_MAXLENGTH,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(AuthSerializer):
    confirmation_code = serializers.CharField(
        max_length=AUTH_CONF_CODE_MAXLENGTH,
        required=True
    )

    def validate(self, data):
        try:
            username = data.get('username')
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f'Пользователя с именем {username} не существует.'
            )
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Некорректный код подтверждения.')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
