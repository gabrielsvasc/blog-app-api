"""Serializer para a rota de Comentários da API."""

from rest_framework import serializers
from rest_framework.request import Request
from core.models import Comment
from utils.validations import ValidateSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer para a tabela Comment."""
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'post', 'reply_to']
        read_only_fields = ['id', 'post', 'reply_to']
