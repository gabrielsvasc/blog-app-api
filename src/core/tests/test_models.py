"""Teste para os Models da API."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch
from decimal import Decimal

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Teste dos models"""

    def test_create_user_with_email_successful(self):
        """Testa a criação de um User com sucesso."""
        email_test = "test@test.com"
        password_test = "test123"
        user = get_user_model().objects.create_user(
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
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)
