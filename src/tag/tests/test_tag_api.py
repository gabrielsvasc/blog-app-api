"""Testes para a rota Tags da API."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from tag.serializers import TagSerializer

TAG_PUBLIC_URL = reverse('tag:public-list')
TAG_CREATE_URL = reverse('tag:private-create')


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


def delete_url(tag: str):
    """Retorna a rota de delete da Tag."""
    return reverse('tag:private-delete', args=[tag])


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

    def test_post_method_auth_required(self):
        """Testa a necessidade de autenticação no método POST."""
        _payload = {
            'user':  self.user,
            'tag': 'Filmes'
        }

        res = self.client.post(TAG_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_method_auth_required(self):
        """Testa a necessidade de autenticação no método DELETE."""
        _tag = create_tag(
            user=self.user,
            tag='tag'
        )

        url = delete_url(_tag.tag)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """Testes de requisições autenticadas."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_tag_create_success(self):
        """Testa uma requisição com sucesso para a rota create."""
        _payload = {
            'user':  self.user,
            'tag': 'Filmes'
        }

        res = self.client.post(TAG_CREATE_URL, _payload)
        _tag = Tag.objects.get(tag=res.data['tag'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(tag=res.data['tag']).exists())
        self.assertEqual(_tag.user, self.user)

    def test_tag_create_unvalidated_data(self):
        """Testa uma requisição para a rota create com dados inválidos."""
        _payload = {
            'user':  self.user,
        }

        res = self.client.post(TAG_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_tag_success(self):
        """Testa uma requisição com sucesso para a rota delete."""
        _tag = create_tag(
            user=self.user,
            tag='tag'
        )

        url = delete_url(_tag.tag)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tag.objects.filter(tag=_tag.tag).exists())

    def test_delete_tag_return_404(self):
        """Testa o retorno do status code 404 quando o post informado não existe."""
        url = delete_url('NExiste')
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_tag_with_other_user(self):
        """Testa o delete permitido apenas para o usuário atrelado ao Post."""
        _user = create_user(
            email='user2@test.com',
            password='pass123'
        )
        _tag = create_tag(
            user=_user,
            tag='tag'
        )

        url = delete_url(_tag.tag)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Tag.objects.filter(tag=_tag.tag).exists())
