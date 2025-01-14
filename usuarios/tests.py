from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from usuarios.models import Morador, UserProfileExample


class MoradorViewSetTestCase(TestCase):
    """Testes para o MoradorViewSet."""

    def setUp(self):
        self.client = APIClient()
        self.valid_data = {
            "cpf": "12345678901",
            "nome": "morador_teste",
            "email": "morador@teste.com",
            "telefone": "999999999",
            "login": "morador_teste",
            "senha": "senha12345",
        }

    def test_create_morador_success(self):
        response = self.client.post("/Moradores/", self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Info", response.data)
        self.assertEqual(response.data["Info"], "Morador criado!")

    def test_create_morador_duplicate_username(self):
        User.objects.create_user(username="morador_teste", password="senha12345")
        response = self.client.post("/Moradores/", self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Nome de usuário já existe.")

    def test_create_morador_missing_data(self):
        incomplete_data = {"nome": "morador_teste"}
        response = self.client.post("/Moradores/", incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cpf", response.data)

    def test_list_moradores(self):
        user = User.objects.create_user(username="morador_teste", password="senha12345")
        Morador.objects.create(nome="Teste Morador", cpf="12345678901", user=user)
        response = self.client.get("/Moradores/listar/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Info", response.data)
        self.assertEqual(len(response.data["data"]), 1)

    def test_delete_morador(self):
        user = User.objects.create_user(username="morador_teste", password="senha12345")
        morador = Morador.objects.create(nome="Teste Morador", cpf="12345678901", user=user)
        response = self.client.delete(f"/Moradores/deletar/?id={morador.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username="morador_teste").exists())
        self.assertFalse(Morador.objects.filter(cpf="12345678901").exists())