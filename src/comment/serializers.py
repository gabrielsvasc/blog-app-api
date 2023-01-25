"""Serializer para a rota de Comentários da API."""

from rest_framework import serializers
from core.models import Comment, Post, User
from post.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer para a tabela Comment."""
    post = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'reply_to', 'post']
        read_only_fields = ['id', 'user']

    @staticmethod
    def get_user(user_id: int) -> User:
        """Retorna a instância do usuário da requisição."""
        return User.objects.get(id=user_id)
