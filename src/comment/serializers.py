"""Serializer para a rota de Comentários da API."""

from rest_framework import serializers
from rest_framework.fields import IntegerField
from core.models import Comment, Post, User
from post.serializers import PostSerializer


def validate_reply(comment_id: int):
    """
        Valida se o id de comentário passado no reply_to existe.
        Se não existir: raise serializers.ValidationError.
    """
    if not Comment.objects.filter(id=comment_id):
        raise serializers.ValidationError(
            'Comentário informado não existe!')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer para a tabela Comment."""
    post = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Post.objects.all())

    reply_to = IntegerField(validators=[validate_reply])

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'reply_to', 'post']
        read_only_fields = ['id', 'user']

    @staticmethod
    def get_user(user_id: int) -> User:
        """Retorna a instância do usuário da requisição."""
        return User.objects.get(id=user_id)
