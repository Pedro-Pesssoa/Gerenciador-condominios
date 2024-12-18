from typing import Any
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from condominio.api.serializers import CondominioSerializer, CasaSerializer
from condominio.models import CondominioModel, CasaModel


class CasaViewSet(ModelViewSet):
    """ViewSet para gerenciar Casas."""
    serializer_class = CasaSerializer
    permission_classes = [AllowAny]
    queryset = CasaModel.objects.all()

    def create(self, request):
        """Sobrescreve o método `create` para gerenciar
        casas."""
        serializer = CasaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        numero = serializer.validated_data['numero']
        bloco = serializer.validated_data['bloco']

        in_database = CasaModel.objects.filter(
            numero=numero,
            bloco=bloco).exists()
        try:
            if not in_database:
                nova_casa = CasaModel.objects.create(
                    numero=serializer.validated_data['numero'],
                    bloco=serializer.validated_data['bloco'],
                    quantidade_quartos=serializer.validated_data[
                        'quantidade_quartos'],
                    quantidade_banheiros=serializer.validated_data[
                        'quantidade_banheiros'],
                    area_lazer=serializer.validated_data['area_lazer'],
                    garagem=serializer.validated_data['garagem'],
                    disponivel=serializer.validated_data['disponivel'],
                )

                serializer_saida = CasaSerializer(nova_casa)
                return Response(
                    {"Info": "Casa criada!",
                     "data": serializer_saida.data},
                    status=status.HTTP_201_CREATED)

            else:
                return Response(
                    {"Info": "Falha ao tentar cadastrar a casa!"},
                    status=status.HTTP_409_CONFLICT)

        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)

        except ValueError:
            return Response(
                {"Info": "A sala já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)

        except Exception:
            return Response(
                {"Erro": "Comportamento Inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False, url_path="buscar")
    def buscar_casa(self):
        """Ação para buscar uma casa pelo nome."""

        try:
            busca = CasaModel.objects.filter(bloco=2)
            serializer = CasaSerializer(busca, many=True)

            return Response(
                {"Info": "Lista de Casas",
                 "data": serializer.data},
                status=status.HTTP_200_OK)

        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)

        except ValueError:
            return Response(
                {"Info": "A sala já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)

        except Exception:
            return Response(
                {"Erro": "Comportamento Inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=False, url_path="deletar")
    def deletar_casa(self, request):
        """Ação para deletar uma casa pelo ID."""
        numero = request.query_params.get('numero', None)

        if numero is not None:
            try:
                casa = CasaModel.objects.get(numero=numero)
                casa.delete()

                return Response(
                    {"Info": "Casa deletada com sucesso!"},
                    status=status.HTTP_204_NO_CONTENT)

            except CasaModel.DoesNotExist:
                return Response(
                    {"Info": "Casa não encontrada!"},
                    status=status.HTTP_404_NOT_FOUND)

            except KeyError:
                return Response(
                    {"Erro": "Algum dado faltando ou errado."},
                    status=status.HTTP_400_BAD_REQUEST)

            except PermissionDenied:
                return Response(
                    {"Erro": "Você não possui permissões para isso."},
                    status=status.HTTP_403_FORBIDDEN)

            except ValueError:
                return Response(
                    {"Info": "A sala já foi cadastrada antes!"},
                    status=status.HTTP_409_CONFLICT)

            except Exception:
                return Response(
                    {"Erro": "Comportamento Inesperado."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(
                {"Info": "Número da casa não fornecido!"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path="listar")
    def listar_casas(self):
        """Ação para listar todas as casas."""

        try:
            casas = CasaModel.objects.all()
            serializer = CasaSerializer(casas, many=True)

            return Response(
                {"Info": "Lista de Casas", "data": serializer.data},
                status=status.HTTP_200_OK)

        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)

        except ValueError:
            return Response(
                {"Info": "A sala já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)

        except Exception:
            return Response(
                {"Erro": "Comportamento Inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CondominioViewSet(ModelViewSet):
    """ViewSet para gerenciar comdominios."""
    serializer_class = CondominioSerializer
    permission_classes = [AllowAny]
    queryset = CondominioModel.objects.all()

    def create(self, request):
        """Sobrescreve o método `create` para gerenciar
        com dominio e casas associadas."""
        serializer = CondominioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:

            casa_numero = serializer.validated_data['casa_numero']
            endereco = serializer.validated_data['endereco']

            sala_existe = CasaModel.objects.filter(numero=casa_numero).exists()
            in_conflict = CondominioModel.objects.filter(
                casa_numero=casa_numero,
                endereco=endereco).exists()

            if sala_existe and not in_conflict:
                novo_condominio = CondominioModel.objects.create(
                    casa_numero=serializer.validated_data['casa_numero'],
                    endereco=serializer.validated_data['endereco'],
                )

                serializer_saida = CondominioSerializer(novo_condominio)

                return Response(
                    {"Info": "Condominio cadastrado!",
                     "data": serializer_saida.data},
                    status=status.HTTP_201_CREATED)

            else:
                return Response(
                    {"Info": "Falha ao tentar cadastrar o condominio!"},
                    status=status.HTTP_409_CONFLICT)

        except KeyError:
            return Response(
                {"Erro": "Algum dado faltando ou errado."},
                status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            return Response(
                {"Erro": "Você não possui permissões para isso."},
                status=status.HTTP_403_FORBIDDEN)

        except ValueError:
            return Response(
                {"Info": "A sala já foi cadastrada antes!"},
                status=status.HTTP_409_CONFLICT)

        except Exception:
            return Response(
                {"Erro": "Comportamento Inesperado."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
