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


class CommentViewSet(viewsets.ViewSet):
    """View para as rotas públicas do Comment."""
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_permissions(self):
        """Define as permissões utilizadas nas rotas."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request: Request) -> Response:
        """Retorna uma lista com todos os comentários criados."""
        serializer: CommentSerializer = self.serializer_class(
            instance=self.queryset,
            many=True
        )

        return Response(serializer.data)
