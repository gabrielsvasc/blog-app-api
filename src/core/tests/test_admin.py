"""Testes para a área do Django Admin."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    "Testes para o Django Admin."

    def setUp(self):
        "Cria o User Autenticado e o Client para os testes."
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@test.com',
            password='test123',
            name='test user'
        )

    def test_user_list(self):
        """Testa o GET com sucesso na rota de User Changelist."""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Testa o GET com sucesso na rota de User Change."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Testa o GET com sucesso na rota de User Add."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
