"""Views para a rota User da API."""

from rest_framework import generics

from user.serializeres import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """View para criação de User."""
    serializer_class = UserSerializer
