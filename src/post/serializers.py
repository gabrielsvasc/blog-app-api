"""Serializer para a rota de Posts da API."""
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.models import Post

from io import BytesIO
from PIL import Image


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

    def resize_image(self, image: InMemoryUploadedFile) -> InMemoryUploadedFile:
        """
            Recebe uma imagem válida em memória e a redimensiona (1080x608).

            Retornos:
                InMemoryUploadedFile -> Fluxo concluído com sucesso.
                Exception -> Erro no fluxo de redimensionar/salvar imagem.

        """
        try:
            buffer = BytesIO()
            temp_image = Image.open(image)
            temp_image = temp_image.resize((1080, 608), Image.LANCZOS)
            temp_image.save(buffer, "webp")

            temp_file = InMemoryUploadedFile(buffer, None, image.name,
                                             'image/webp', buffer.tell(), None)
            return temp_file

        except Exception as ex:
            raise ex('Resize Image: erro durante redimencionamento de imagem.')

    def update(self, instance: Post, validated_data: dict) -> Post:
        """
        Overwrite do método Update para ajustar campo Image.

        Retornos:
            Post -> Instância atualizada com sucesso.
            Exception -> Falha no método resize_image.
        """

        if validated_data.get('image'):
            image = validated_data['image']
            instance.image.delete(save=True)
            validated_data['image'] = self.resize_image(image)

        return super().update(instance, validated_data)

    def save(self, **kwargs) -> Post:
        """
        Overwrite do método Save para ajustar campo Image.

        Retornos:
            Post -> Instância salva com sucesso.
            Exception -> Falha no método resize_image.
        """
        if self.validated_data['image']:
            image = self.validated_data['image']
            self.validated_data['image'] = self.resize_image(image)

        return super().save(**kwargs)
