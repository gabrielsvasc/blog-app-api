"""Serializer para a rota de Posts da API."""

from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer para a rota de Posts."""
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc_post', 'datetime']
        read_only_fields = ['id']
