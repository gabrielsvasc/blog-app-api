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


class TagPrivateViewSet(viewsets.ViewSet):
    """View usada para todos os métodos privados."""
    queryset = Tag.objects.all().order_by('-tag')
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:
        """
            Recebe os dados da Tag que será criada e retorna um status conforme condições: \n
                201 - Objeto criado com sucesso. \n
                400 - Dados passados não são válidos. \n
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
