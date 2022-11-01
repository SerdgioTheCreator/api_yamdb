from rest_framework import serializers

from reviews.models import Categories, Genry, Title


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenrySerializers(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genry


class TitleSerializers(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title
