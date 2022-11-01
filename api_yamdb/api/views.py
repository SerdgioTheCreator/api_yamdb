from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Review
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer


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