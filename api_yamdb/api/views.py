from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review, Title
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        ).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id')
        )
