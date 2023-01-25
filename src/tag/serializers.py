"""Serializer para a rota de Tags da API."""

from rest_framework import serializers
from rest_framework.request import Request
from core.models import Tag
from utils.validations import ValidateSerializer


class TagSerializer(serializers.ModelSerializer):
    """Serializer para a tabela de Tags."""
    class Meta:
        model = Tag
        fields = ['tag']
