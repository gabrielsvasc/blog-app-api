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


class PublicPostApiTests(TestCase):
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
