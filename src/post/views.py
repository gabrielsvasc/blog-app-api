"""Views para a rota de Posts da API."""
from rest_framework import viewsets, mixins, status, generics
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

from core.models import Post
from post.serializers import PostSerializer, PostDetailSerializer


class PostPrivateViewSet(
        viewsets.ViewSet):
    """View para as rotas privadas do Post."""
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def publish(self, request: Request) -> Response:
        """
            Recebe os dados do Post que será criado e retorna um status conforme condições: \n
                201 - Objeto criado com sucesso. \n
                400 - Dados passados não são válidos. \n
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update_post(self, request: Request, pk: int = None):
        """
            Recebe os dados do Post que será atualizado e retorna um status conforme condições: \n
                200 - Objeto atualizado com sucesso. \n
                400 - Dados passados não são válidos. \n
                401 - Usuário da requisição não tem permissão para atualizar esse objeto. \n
                404 - Objeto não existe no banco de dados. \n
        """
        _post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            instance=_post, data=request.data, partial=True)

        if serializer.is_valid():
            if serializer.is_valid_user(_post, request):
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.data, status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete_post(self, request: Request, pk: int = None):
        """
            Recebe o ID do Post que será deletado e retorna um status conforme condições: \n
                204 - Objeto deletado com sucesso. \n
                401 - Usuário da requisição não tem permissão para deletar esse objeto. \n
                404 - Objeto não existe no banco de dados. \n
        """
        _post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            instance=_post
        )

        if serializer.is_valid_user(_post, request):
            _post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PostPublicViewSet(viewsets.ViewSet):
    """View para as rotas públicas do Post."""
    queryset = Post.objects.all().order_by('-id')
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self) -> PostSerializer | PostDetailSerializer:
        """Define o Serializer usado em cada método."""
        if self.action == 'list':
            return PostSerializer
        else:
            return PostDetailSerializer

    def list(self, request: Request) -> Response:
        """Retorna uma lista com todos os Posts resumidos."""
        _get_serializer = self.get_serializer_class()
        serializer: PostSerializer = _get_serializer(self.queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        """
            Retorna um post detalhado se o objeto informado existir: \n
                204 - Objeto retornado com sucesso. \n
                404 - Objeto não existe no banco de dados. \n
        """
        _get_serializer = self.get_serializer_class()
        _post = get_object_or_404(self.queryset, pk=pk)
        serializer: PostDetailSerializer = _get_serializer(_post)

        return Response(serializer.data)
