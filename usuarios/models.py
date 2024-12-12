from django.db import models
from django.contrib.auth.models import User


class UserProfileExample(models.Model):
    """Model para perfil de usuário com informações adicionais."""
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=150)
    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """Nomeclatura para Classe"""
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Morador(models.Model):
    """Model para moradores associados a usuários."""
    nome = models.CharField(max_length=140)
    cpf = models.CharField(max_length=16, unique=True)
    telefone = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        """Nomeclatura para Classe"""
        verbose_name = "Morador"
        verbose_name_plural = "Moradores"

    def __str__(self):
        return self.nome
