"""Serializer para a rota User da API."""

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o User."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data: dict) -> User:
        """Cria e retorna um User com password criptografado."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data: dict) -> User:
        """Atualiza e retorna um User."""
        password = validated_data.pop('password', None)
        user: User = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer para o User Auth Token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs: dict) -> dict:
        """Valida e autentica um User."""
        _email = attrs.get('email')
        _password = attrs.get('password')
        _user = authenticate(
            request=self.context.get('request'),
            username=_email,
            password=_password,
        )

        if not _user:
            _msg = _('Não foi possível validar as credenciais.')
            raise serializers.ValidationError(_msg, code='authorization')

        attrs['user'] = _user
        return attrs
