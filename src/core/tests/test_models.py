"""Teste para os Models da API."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch
from decimal import Decimal

from core import models


def create_user(email, password):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create_user(email, password)


def create_post(user, title, desc_post, post):
    """Cria e retorna um novo usuário."""
    return models.Post.objects.create(
        user=user,
        title=title,
        desc_post=desc_post,
        post=post
    )


class ModelTests(TestCase):
    """Teste dos models"""

    def test_create_user_with_email_successful(self):
        """Testa a criação de um User com sucesso."""
        email_test = "test@test.com"
        password_test = "test123"
        user = create_user(
            email=email_test,
            password=password_test,
        )

        self.assertEqual(user.email, email_test)
        self.assertTrue(user.check_password(password_test))

    def test_new_user_with_email_normalized(self):
        """Testa a normalização do campo de e-mail."""
        sample_emails = [
            ['test1@test.com', 'test1@test.com'],
            ['Test2@Test.com', 'Test2@test.com'],
            ['Test3@test.com', 'Test3@test.com'],
            ['test4@Test.com', 'test4@test.com'],
            ['TEST5@TEST.COM', 'TEST5@test.com'],
            ['TEST6@test.com', 'TEST6@test.com'],
            ['test7@TEST.com', 'test7@test.com'],
            ['test8@test.COM', 'test8@test.com'],
        ]

        for email, expected in sample_emails:
            user = create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Testa a criação de User sem e-mail Raise ValueError."""
        with self.assertRaises(ValueError):
            create_user('', 'test123')

    def test_create_superuser_success(self):
        """Testa a criação de Superuser com sucesso."""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_post(self):
        """Testa a criação de um post com sucesso."""
        _user = create_user(
            'test@example.com',
            'testpass123',
        )
        _post = models.Post.objects.create(
            user=_user,
            title='Test Title',
            desc_post='Test Desc',
            post='Test Post'
        )

        self.assertEqual(str(_post), _post.title)

    def test_create_tag(self):
        """Testa a criação de uma tag com sucesso."""
        _user = create_user(
            'test@example.com',
            'testpass123',
        )
        _tag = models.Tag.objects.create(
            user=_user,
            tag='Esportes'
        )

        self.assertEqual(str(_tag), _tag.tag)

    def test_create_comment(self):
        """Testa a criação de um comentário com sucesso no banco de dados."""
        _user = create_user(
            'test@example.com',
            'testpass123',
        )
        _post = create_post(
            _user,
            'test',
            'test desc',
            'post test'
        )
        _comment = models.Comment.objects.create(
            user=_user,
            post=_post,
            comment='Teste Comment',
            reply_to=1,
        )

        self.assertEqual(str(_comment), _comment.comment)
