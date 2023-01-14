"""Serializer para a rota de Posts da API."""

from rest_framework import serializers
from rest_framework.request import Request
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer para a rota de Posts."""
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc_post', 'datetime']
        read_only_fields = ['id']


class PostDetailSerializer(PostSerializer):
    """Serializer para o detalhamento do Post."""
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['post']

    def is_valid_user(self, instance: Post, request: Request) -> bool:
        """Valida se o usuário da requisição é o mesmo do objeto:
        Se forem iguais retorna True.
        Se forem diferente retorna False."""
        serializer_user = instance.user
        request_user = request.user

        if (serializer_user == request_user):
            return True

        return False
