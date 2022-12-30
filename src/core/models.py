"""Models da API."""

from __future__ import annotations
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Gerenciador dos Users."""

    def create_user(self, email: str, password: str = None, **kwargs) -> User:
        """Cria, salva e retorna um novo User."""
        user: User = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model para User da API."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
