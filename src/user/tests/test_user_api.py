"""Testes para a rota de User da API."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')


def create_user(**params):
    """Cria e retorna um novo usuário."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Testes das rotas públicas da API. (sem autenticação)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Testa a criação de um usuário com sucesso."""
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Testa a criação de usuário com e-mail já existente."""
        payload = {
            'email': 'test@test.com',
            'password': 'test123',
            'name': 'Test Test',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Testa criação de um usuário com senha menor que 5 caracteres."""
        payload = {
            'email': 'test2@test.com',
            'password': 'pw',
            'name': 'Test Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Testa a geração do token com as credenciais."""
        user_details = {
            'name': 'Test Name',
            'email': 'test.token@example.com',
            'password': 'test@Pass123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Testa retorno de erro para credenciais invalidas."""
        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@test.com',
            'password': 'wrongtest123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Testa Token com senha em branco retorna erro."""
        payload = {
            'email': 'test@test.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
