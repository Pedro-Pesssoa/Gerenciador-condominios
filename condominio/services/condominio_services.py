from condominio.models import CondominioModel

class CondominioService:

        def create(self, data):
            numero=data['casa_numero']
            endereco=data['endereco']

            in_database = CondominioModel.objects.filter(
                  numero=numero,
                  endereco=endereco).exists()
            
            if in_database:
                raise ValueError
            else:
                novo_condominio = CondominioModel.objects.create(
                    numero=data['casa_numero'],
                    endereco=data['endereco']
                 )
            return novo_condominio


