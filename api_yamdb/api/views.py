from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Categories, Genre, Title, Review
from .permissions import IsAuthorOrReadOnly
from .serializers import CategoriesSerializer, GenreSerializers, TitleSerializers, CommentSerializer


class TitleListView(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializers


class GenreListView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class CategoriesListView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('title_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_id')
        )