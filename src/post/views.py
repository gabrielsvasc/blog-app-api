"""Views para a rota de Posts da API."""
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Post
from post.serializers import PostSerializer, PostDetailSerializer


class PostListViewSet(viewsets.ViewSet):
    """ViewSet para a rota Post."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def list(self, request: any) -> PostSerializer:
        """Retorna todos os Posts de forma resumida."""
        queryset = Post.objects.all().order_by('-id')
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: any, pk: int = None) -> PostDetailSerializer:
        """Retorna apenas um Post com todos detalhes."""
        queryset = Post.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(user)

        return Response(serializer.data)
