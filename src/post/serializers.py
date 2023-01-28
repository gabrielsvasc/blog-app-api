"""Serializer para a rota de Posts da API."""
import os
from rest_framework import serializers
from rest_framework.request import Request
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer para a tabela de Posts."""
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc_post', 'datetime']
        read_only_fields = ['id']


class PostDetailSerializer(PostSerializer):
    """Serializer para o detalhamento do Post."""
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['post']


class PostImageSerializer(serializers.ModelSerializer):
    """Serializer para o upload de imagens."""

    class Meta:
        model = Post
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
