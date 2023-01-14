"""Views para a rota de Posts da API."""
from rest_framework import viewsets, mixins, status, generics
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

from core.models import Tag
from tag.serializers import TagSerializer


class TagPublicViewSet(viewsets.ViewSet):
    """View usada para listar as Tags."""

    queryset = Tag.objects.all().order_by('-tag')
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def list(self, request: Request) -> Response:
        """Retorna uma lista com todas as Tags criadas."""
        serializer: TagSerializer = self.serializer_class(
            self.queryset, many=True)

        return Response(serializer.data)
