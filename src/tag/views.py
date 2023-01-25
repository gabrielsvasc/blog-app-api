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
from utils.validations import ValidateSerializer


class TagViewSet(viewsets.ViewSet):
    """View usada para listar as Tags."""

    queryset = Tag.objects.all().order_by('-tag')
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    validate = ValidateSerializer()

    def get_permissions(self):
        """Define as permissões utilizadas nas rotas."""
        if self.action in ['list']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request: Request) -> Response:
        """Retorna uma lista com todas as Tags criadas."""
        serializer: TagSerializer = self.serializer_class(
            self.queryset, many=True)

        return Response(serializer.data)

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

    def delete(self, request: Request, pk: str = None):
        """
            Recebe a Tag que será deletada e retorna um status conforme condições: \n
                204 - Objeto deletado com sucesso. \n
                401 - Usuário da requisição não tem permissão para deletar esse objeto. \n
                404 - Objeto não existe no banco de dados. \n
        """
        _tag = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            instance=_tag)

        if self.validate.is_valid_user(_tag.user, request.user):
            _tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.data, status.HTTP_401_UNAUTHORIZED)

    def update(self, request: Request, pk: str = None):
        """
            Recebe a Tag que será atualizada e retorna um status conforme condições: \n
                200 - Objeto atualizado com sucesso. \n
                400 - Dados da requisição não são validos. \n
                401 - Usuário da requisição não tem permissão para deletar esse objeto. \n
                404 - Objeto não existe no banco de dados. \n
        """
        _tag = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            instance=_tag, data=request.data, partial=False)

        if serializer.is_valid():
            if self.validate.is_valid_user(_tag.user, request.user):
                serializer.update(_tag, request.data)

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.data, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
