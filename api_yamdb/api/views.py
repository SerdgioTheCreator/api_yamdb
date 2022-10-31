from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from reviews.models import Categories, Genry, Title
from .serializers import CategoriesSerializer, GenrySerializers, TitleSerializers


class TitleListView(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializers


class GenryListView(viewsets.ModelViewSet):
    queryset = Genry.objects.all()
    serializer_class = GenrySerializers


class CategoriesListView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
