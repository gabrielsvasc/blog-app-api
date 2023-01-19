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

    def is_valid_user(self, instance: Tag, request: Request) -> bool:
        """
        Valida se o usuário da requisição é valido.

        Retorna:
            bool: obtem o retorno da ValidateSerializer.
        """
        serializer_user = instance.user
        request_user = request.user

        is_valid = ValidateSerializer.is_valid_user(
            serializer_user, request_user)

        return is_valid

    def update(self, instance: Tag, validated_data: Request) -> None:
        """
            Recebe uma instance que deve ser atualizada e os dados que serão utilizados.

            instance: Tag (registro que será alterado).
            validated_data: Request (dados utilizados para alteração).
        """
        Tag.objects.filter(tag=instance.tag).update(tag=validated_data['tag'])
