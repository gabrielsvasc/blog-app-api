"""Models da API."""

from __future__ import annotations

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    """Gerenciador dos Users."""

    def create_user(self, email: str, password: str = None, **kwargs) -> User:
        """Cria, salva e retorna um novo User."""
        if not email:
            raise ValueError('ERRO: User precisa de um e-mail válido.')

        user: User = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str) -> User:
        """Cria, salva e retorna um Superuser."""
        _user = self.create_user(email=email, password=password)

        _user.is_staff = True
        _user.is_superuser = True
        _user.save(using=self._db)

        return _user


class User(AbstractBaseUser, PermissionsMixin):
    """Model para Users da API."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Post(models.Model):
    """Model para Posts da API."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    desc_post = models.TextField()
    post = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    """Model para Posts da API."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    tag = models.CharField(max_length=40, primary_key=True)

    def __str__(self) -> str:
        return self.tag


class Comment(models.Model):
    """Model para Comentários da API."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             )
    comment = models.TextField()
    reply_to = models.BigIntegerField(default=None)

    def __str__(self) -> str:
        return self.comment
