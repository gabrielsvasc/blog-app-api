"""Views para a rota de Posts da API."""
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Post
from post import serializers


class PostListViewSet(
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """ViewSet para a rota Post."""
    serializer_class = serializers.PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self) -> Post:
        return self.queryset.order_by('-id')
