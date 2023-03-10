"""Testes para a rota Comment da API."""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Comment, Post
from comment.serializers import (
    CommentSerializer
)

COMMENT_LIST_URL = reverse('comment:comment-list')
COMMENT_CREATE_URL = reverse('comment:comment-create')


def patch_url(comment_id: int):
    """Retorna a rota patch de um comentário."""
    return reverse('comment:comment-update', args=[comment_id])


def delete_url(comment_id: int):
    """Retorna a rota patch de um comentário."""
    return reverse('comment:comment-delete', args=[comment_id])


def create_user(email='user@example.com', password='testpass123'):
    """Cria e retorna um novo usuário."""

    return get_user_model().objects.create_user(email=email, password=password)


def create_comment(user, post, comment, reply_to=None):
    """Cria e retorna um novo comentário."""
    comment = Comment.objects.create(
        user=user,
        post=post,
        comment=comment,
        reply_to=reply_to
    )

    return comment


def create_post(user, title, desc_post, post) -> Post:
    """Cria e retorna um novo Post."""
    post = Post.objects.create(
        user=user,
        title=title,
        desc_post=desc_post,
        post=post
    )

    return post


class PublicCommentApiTests(TestCase):
    """Testes de requisições não autenticadas."""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()

    def test_retrieve_comments(self):
        """Testa o retorno com os Comentários listados."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        create_comment(
            user=self.user,
            post=_post,
            comment='comments 1'
        )
        create_comment(
            user=self.user,
            post=_post,
            comment='comments 2'
        )

        res = self.client.get(COMMENT_LIST_URL)

        comments = Comment.objects.all().order_by('-id')
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_comments(self):
        """Testa o retorno dos Comentários."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        create_comment(
            user=self.user,
            post=_post,
            comment='comments 1'
        )
        create_comment(
            user=self.user,
            post=_post,
            comment='comments 2'
        )

        res = self.client.get(COMMENT_LIST_URL)

        comments = Comment.objects.all().order_by('-id')
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_comments_from_all_users(self):
        """Testa o retorno dos Comentários indepentente do usuário."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _user = create_user(
            email='teste@mail.com',
            password='gfdsgfs'
        )
        create_comment(
            user=self.user,
            post=_post,
            comment='comments 1'
        )
        create_comment(
            user=_user,
            post=_post,
            comment='comments 2'
        )

        res = self.client.get(COMMENT_LIST_URL)

        comments = Comment.objects.all().order_by('-id')
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))

    def test_comment_post_method_auth_required(self):
        """Testa a necessidade de autenticação no método POST."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'post': _post.id,
            'comment': 'comments 1',
            'reply_to': _comment.id
        }

        res = self.client.post(COMMENT_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_patch_method_auth_required(self):
        """Testa a necessidade de autenticação no método PATCH."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'comment': 'comments 1'
        }

        url = patch_url(_comment.id)
        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete_method_auth_required(self):
        """Testa a necessidade de autenticação no método DELETE."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )

        url = delete_url(_comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCommentApiTests(TestCase):
    """Testes de requisições não autenticadas."""

    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_post_comment_success(self):
        """Testa a criação de um comentário com sucesso."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'post': _post.id,
            'comment': 'comments 1',
            'reply_to': _comment.id
        }

        res = self.client.post(COMMENT_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_post_comment_unvalidated_data(self):
        """Testa uma tentativa de criação de comentário com dados inválidos."""
        _payload = {
            'comment': 'comments 1',
            'reply_to': 1
        }
        res = self.client.post(COMMENT_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_comment_reply_to_unexistent_comment(self):
        """
        Testa comentário com reply_to inválido.
        """
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'post': _post.id,
            'comment': 'comments 1',
            'reply_to': _comment.id + 1
        }

        res = self.client.post(COMMENT_CREATE_URL, _payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_success(self):
        """Testa um update com sucesso em um comentário."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'comment': 'comments 1',
        }

        url = patch_url(_comment.id)
        res = self.client.patch(url, _payload)
        _comment.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(_payload['comment'], _comment.comment)

    def test_patch_comment_return_404(self):
        """Testa o retorno do status code 404 quando o comentário informado não existe."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )
        _payload = {
            'comment': 'comments 1',
        }
        url = patch_url(_comment.id+1)
        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_comment_with_other_user(self):
        """Testa o update permitido apenas para o usuário atrelado ao comentário."""
        _user = create_user(
            email='user2@test.com',
            password='pass123'
        )
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=_user,
            post=_post,
            comment='test'
        )
        _payload = {
            'comment': 'comments 1',
        }

        url = patch_url(_comment.id)
        res = self.client.patch(url, _payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_success(self):
        """Testa uma requisição com sucesso no método DELETE."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )

        url = delete_url(_comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=_comment.id).exists())

    def test_delete_comment_return_404(self):
        """Testa o retorno do status code 404 quando o comentário informado não existe."""
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=self.user,
            post=_post,
            comment='test'
        )

        url = delete_url(_comment.id+1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_with_other_user(self):
        """Testa o delete permitido apenas para o usuário atrelado ao comentário."""
        _user = create_user(
            email='user2@test.com',
            password='pass123'
        )
        _post = create_post(
            user=self.user,
            title='title 1',
            desc_post='desc 1',
            post='post 1',
        )
        _comment = create_comment(
            user=_user,
            post=_post,
            comment='test'
        )

        url = delete_url(_comment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Comment.objects.filter(id=_comment.id).exists())
