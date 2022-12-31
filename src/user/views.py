"""Views para a rota User da API."""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializeres import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """View para criação de User."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """View para criação de Auth Token para o User."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
