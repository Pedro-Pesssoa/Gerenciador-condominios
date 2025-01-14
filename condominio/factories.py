from factory import django, Faker, SubFactory
from condominio.models import CasaModel, CondominioModel
import factory

class CasaFactory(django.DjangoModelFactory):
    """Factory para o modelo Casa"""
    class Meta:
        model = CasaModel

    numero = factory.Sequence(lambda n: n + 1)
    bloco = factory.Sequence(lambda n: (n % 5) + 1)
    quantidade_quartos = factory.Faker('random_int', min=1, max=4)
    quantidade_banheiros = factory.Faker('random_int', min=1, max=3)
    area_lazer = factory.Faker('boolean')
    garagem = factory.Faker('boolean')
    disponivel = factory.Faker('boolean')

class CondominioFactory(django.DjangoModelFactory):
    """Factory para o modelo Condominio"""
    class Meta:
        model = CondominioModel

    casa_numero = factory.Sequence(lambda n: n + 1)
    endereco = factory.Faker('address')