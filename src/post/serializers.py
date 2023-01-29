"""Serializer para a rota de Posts da API."""
from rest_framework import serializers
from core.models import Post
from django.core.files.uploadedfile import InMemoryUploadedFile


class PostSerializer(serializers.ModelSerializer):
    """Serializer para a tabela de Posts."""
    class Meta:
        model = Post
        fields = ['id', 'title', 'desc_post', 'image']
        read_only_fields = ['id', 'datetime']


class PostDetailSerializer(PostSerializer):
    """Serializer para o detalhamento do Post."""
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['post']
        extra_kwargs = {'image': {'required': 'True'}}

    def validate_image(self, value: InMemoryUploadedFile):
        """
            Valida a imagem enviada pelo usuário.

            Retornos:
             value.size > 2MB: ValidationError
             value.size < 2MB: InMemoryUploadedFile
        """
        if value.size > 2097152:
            raise serializers.ValidationError(
                'Tamanho da imagem maior do que o permitido. (2MB)')

        return value
