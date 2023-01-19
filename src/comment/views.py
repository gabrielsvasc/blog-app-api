"""Views para a rota de Comentários da API."""
from rest_framework import viewsets, mixins, status, generics
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

from core.models import Comment
from comment.serializers import CommentSerializer


class CommentPublicViewSet(viewsets.ViewSet):
    """View para as rotas públicas do Comment."""
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def list(self, request: Request) -> Response:
        """Retorna uma lista com todos os comentários criados."""
        serializer: CommentSerializer = self.serializer_class(
            instance=self.queryset,
            many=True
        )
        return Response(serializer.data)
