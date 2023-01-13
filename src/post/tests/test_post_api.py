"""Testes para a rota Ingredients da API."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from post.serializers import (
    PostSerializer,
    PostDetailSerializer
)


POST_PUBLIC_URL = reverse('post:public-list')
POST_CREATE_URL = reverse('post:private-publish')


def create_user(email='user@example.com', password='testpass123'):
    """Cria e retorna um novo usuário."""

    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(post_id):
    """Retorna os detalhes de um Post."""
    return reverse('post:public-detail', args=[post_id])


def patch_url(post_id):
    """Retorna a rota patch de um Post."""
    return reverse('post:private-update', args=[post_id])


def delete_url(post_id):
    """Retorna a rota patch de um Post."""
    return reverse('post:private-delete', args=[post_id])


def create_post(user, title, desc_post, post) -> Post:
    """Cria e retorna um novo post."""
    post = Post.objects.create(
        user=user,
        title=title,
        desc_post=desc_post,
        post=post
    )

    return post


class PublicPostApiTests(TestCase):
    """Testes de requisições não autenticadas."""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()

    def test_retrieve_posts(self):
        """Testa o retorno com todos os Posts."""
        create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        create_post(
            user=self.user,
            title='title 2',
            desc_post='desc 2',
            post='post 2',
        )

        res = self.client.get(POST_PUBLIC_URL)

        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_post_detail(self):
        """Testa o retorno com os detalhes do Post desejado."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )

        url = detail_url(_post.id)
        res = self.client.get(url)

        serializer = PostDetailSerializer(_post)
        self.assertEqual(res.data, serializer.data)

    def test_post_method_auth_required(self):
        """Testa a necessidade de autenticação no método POST."""
        _payload = {
            'title': 'Test Title Fail',
            'desc_post': 'Test Description Fail',
            'post': 'Test Post Fail',
        }
        res = self.client.post(POST_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_method_auth_required(self):
        """Testa a necessidade de autenticação no método PATCH."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _payload = {
            'title': 'Test Title Fail'
        }

        url = patch_url(_post.id)

        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_method_auth_required(self):
        """Testa a necessidade de autenticação no método DELETE."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )

        url = delete_url(_post.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePostApiTests(TestCase):
    """Testes de requisições autenticadas."""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_post_publish_success(self):
        """Testa uma requisição com sucesso para a rota publish."""
        _payload = {
            'title': 'Test Title Fail',
            'desc_post': 'Test Description Fail',
            'post': 'Test Post Fail',
        }

        res = self.client.post(POST_CREATE_URL, _payload)
        _post = Post.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(_post.user, self.user)

        for k, v in _payload.items():
            self.assertEqual(getattr(_post, k), v)

    def test_post_publish_unvalidated_data(self):
        """Testa uma requisição para a rota publish com dados inválidos."""
        _payload = {
            'title': 'Test Title Fail',
            'post': 'Test Post Fail',
        }

        res = self.client.post(POST_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_post_success(self):
        """Testa uma requisição com sucesso para a rota update."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _payload = {
            'title': 'Test Title Fail'
        }

        url = patch_url(_post.id)
        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        _post.refresh_from_db()

        self.assertEqual(_post.title, _payload['title'])

    def test_patch_post_with_other_user(self):
        """Testa o update permitido apenas para o usuário atrelado ao Post."""
        _user = create_user(
            email='user2@test.com',
            password='pass123'
        )
        _post = create_post(
            user=_user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _payload = {
            'title': 'Test Title Fail'
        }

        url = patch_url(_post.id)
        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_success(self):
        """Testa uma requisição com sucesso para a rota delete."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )

        url = delete_url(_post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=_post.id).exists())

    def test_delete_post_with_other_user(self):
        """Testa o delete permitido apenas para o usuário atrelado ao Post."""
        _user = create_user(
            email='user2@test.com',
            password='pass123'
        )
        _post = create_post(
            user=_user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )

        url = delete_url(_post.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Post.objects.filter(id=_post.id).exists())
