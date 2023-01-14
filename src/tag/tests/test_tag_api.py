"""Testes para a rota Tags da API."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from tag.serializers import TagSerializer

TAG_PUBLIC_URL = reverse('tag:public-list')


def create_user(email='user@example.com', password='testpass123'):
    """Cria e retorna um novo usuário."""

    return get_user_model().objects.create_user(email=email, password=password)


def create_tag(user, tag) -> Tag:
    """Cria e retorna uma nova Tag."""
    tag = Tag.objects.create(
        user=user,
        tag=tag
    )

    return tag


class PublicTagApiTests(TestCase):
    """Testes de requisições não autenticadas."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()

    def test_retrieve_tags(self):
        """Testa o retorno com sucesso de todas as Tags."""
        create_tag(
            user=self.user,
            tag='Filmes'
        )
        create_tag(
            user=self.user,
            tag='Esportes'
        )

        res = self.client.get(TAG_PUBLIC_URL)

        tags = Tag.objects.all().order_by('-tag')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
