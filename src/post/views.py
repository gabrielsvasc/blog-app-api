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
        """Recebe os valores para criação de um Post, se forem validos retorna HTTP 201
        e se não retorna HTTP 400."""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update_post(self, request: Request, pk: int = None):
        """Recebe os valores para atualização do Post, se forem validos retorna HTTP 201
        e se não retorna HTTP 400."""
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
            Recebe o ID do Post que será deletado e retorna um status conforme condições:
                204 - Objeto deletado com sucesso.
                404 - Objeto não existe no banco de dados.
                401 - Usuário da requisição não tem permissão.
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
        """Retorna um Post específico."""
        _get_serializer = self.get_serializer_class()
        _post = get_object_or_404(self.queryset, pk=pk)
        serializer: PostDetailSerializer = _get_serializer(_post)

        return Response(serializer.data)
