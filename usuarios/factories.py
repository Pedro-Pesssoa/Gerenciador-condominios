from factory import django, Faker, SubFactory
from django.contrib.auth.models import User
from usuarios.models import UserProfileExample, Morador
import factory

class UserFactory(django.DjangoModelFactory):
    """Factory para o modelo User do Django"""
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class UserProfileExampleFactory(django.DjangoModelFactory):
    """Factory para o modelo UserProfileExample"""
    class Meta:
        model = UserProfileExample

    user = SubFactory(UserFactory)
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    birth_date = factory.Faker('date_of_birth', minimum_age=18, maximum_age=90)

class MoradorFactory(django.DjangoModelFactory):
    """Factory para o modelo Morador"""
    class Meta:
        model = Morador

    user = SubFactory(UserFactory)
    nome = factory.Faker('name')
    cpf = factory.Sequence(lambda n: f'{n:011d}')  # Gera CPFs únicos sequenciais
    telefone = factory.Faker('phone_number')