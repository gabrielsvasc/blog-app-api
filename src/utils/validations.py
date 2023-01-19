from rest_framework import serializers
from rest_framework.request import Request
from core.models import Post


class ValidateSerializer(serializers.ModelSerializer):

    @staticmethod
    def is_valid_user(instance_user: Post, request_user: Request) -> bool:
        """
        Valida se o usuário da requisição é o mesmo do objeto.

        Retornos:
            bool: True (se forem iguais) e False (caso contrário).
        """
        if (instance_user == request_user):
            return True

        return False
