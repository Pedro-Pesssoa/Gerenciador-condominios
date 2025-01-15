from django.test import TestCase
from django.contrib.auth.models import User
from usuarios.factories import UserFactory, UserProfileExampleFactory, MoradorFactory
from usuarios.models import Morador, UserProfileExample

class UsuariosTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = UserProfileExampleFactory(user=self.user)
        self.morador = MoradorFactory()

    def test_criar_usuario(self):
        self.assertIsNotNone(self.user.id)
        self.assertTrue(self.user.check_password('password123'))

    def test_criar_profile(self):
        self.assertIsNotNone(self.profile.id)
        self.assertEqual(self.profile.user, self.user)

    def test_criar_morador(self):
        self.assertIsNotNone(self.morador.id)
        self.assertIsNotNone(self.morador.user)
        self.assertTrue(len(self.morador.cpf) == 11)