"""Serializer para a rota de Comentários da API."""

from rest_framework import serializers
from rest_framework.fields import IntegerField
from core.models import Comment, Post, User
from post.serializers import PostSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer para a tabela Comment."""
    post = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Post.objects.all())

    user = serializers.HiddenField(
        write_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'reply_to', 'post', 'user']
        read_only_fields = ['id']

    def validate_reply_to(self, value: int):
        if not Comment.objects.filter(id=value):
            raise serializers.ValidationError(
                'Comentário informado não existe!')
