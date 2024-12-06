from rest_framework import serializers
from usuarios.models import Morador, UserProfileExample


class UserProfileExampleSerializer(serializers.ModelSerializer):
    """Serializer para o modelo UserProfileExample."""
    class Meta:
        model = UserProfileExample
        fields = ['id', 'address', 'phone_number', 'birth_date', 'user']


class MoradorSerializer(serializers.ModelSerializer):
    """Serializer para operações gerais do modelo Morador."""
    class Meta:
        model = Morador
        fields = "__all__"


class MoradorCreateSerializer(serializers.Serializer):
    """Serializer para criação de moradores."""
    nome = serializers.CharField(max_length=140)
    cpf = serializers.CharField(max_length=16)
    telefone = serializers.CharField(max_length=20)
    login = serializers.CharField(max_length=100)
    senha = serializers.CharField(max_length=100)
