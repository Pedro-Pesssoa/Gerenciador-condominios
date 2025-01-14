from django.contrib.auth.models import User, Group

from usuarios.models import Morador

class MoradorService:

    def create(self, data):
        novo_user = User.objects.create_user(
            username=data['login'],
            password=data['senha'],
        )
        grupo_moradores, _ = Group.objects.get_or_create(nome="Moradores")
        novo_user.group.add(grupo_moradores)

        novo_morador = Morador.objects.create(
            nome=data['nome'],
            cpf=data['cpf'],
            telefone=data['telefone'],
            user=novo_user

        )
        return novo_morador
    