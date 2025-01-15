from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from condominio.models import CasaModel
from condominio.factories import CasaFactory, CondominioFactory

# Create your tests here.

class CasaTesteCase(TestCase):

    def setUp(self):
        self.casa = CasaFactory()

    def test_cadastrar_casas(self):

        url = "http://localhost:8000/casas/"
        casa = CasaFactory(
            numero=2,
            bloco=2,
            quantidade_quartos=1,
            quantidade_banheiros=2,
            area_lazer=True,
            garagem=True,
            disponivel=True
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['numero'], 2)

    def test_listar_casas(self):

        url = "http://localhost:8000/casas/"
        data = {
            "numero": 2,
            "bloco": 2,
            "quantidade_quartos": 1,
            "quantidade_banheiros": 2,
            "area_lazer": True,
            "garagem": True,
            "disponivel": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CasaModel.objects.filter(numero=2, bloco=2).exists())

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

class CondominioTesteCase(TestCase):
    def setUp(self):
        self.casa = CasaFactory()
        self.condominio = CondominioFactory(casa_numero=self.casa.numero)

    def test_criar_condominio(self):
        self.assertIsNotNone(self.condominio.id)
        self.assertEqual(self.condominio.casa_numero, self.casa.numero)
