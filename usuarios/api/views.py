from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from usuarios.api.serializers import MoradorCreateSerializer, MoradorSerializer, UserProfileExampleSerializer
from usuarios.models import Morador, UserProfileExample
from django.contrib.auth.models import User
from django.db import IntegrityError


class UserProfileExampleViewSet(ModelViewSet):
    """ViewSet para gerenciar Usuarios."""
    queryset = UserProfileExample.objects.all()
    serializer_class = UserProfileExampleSerializer


class MoradorViewSet(ModelViewSet):
    """ViewSet para gerenciar Moradores."""
    serializer_class = MoradorSerializer
    permission_classes = [AllowAny]
    queryset = Morador.objects.all()

    def create(self, request):
        """Sobrescreve o método `create` para gerenciar
        moradores e usuários associados."""
        serializer = MoradorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login = serializer.validated_data['login']
        senha = serializer.validated_data['senha']

        # Verificar se o nome de usuário já existe
        if User.objects.filter(username=login).exists():
            return Response(
                {"error": "Nome de usuário já existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Criação do usuário associado
            novo_user = User.objects.create_user(
                username=login,
                password=senha,
            )

            # Criação do morador
            novo_morador = Morador.objects.create(
                nome=serializer.validated_data['nome'],
                cpf=serializer.validated_data['cpf'],
                telefone=serializer.validated_data['telefone'],
                user=novo_user
            )

            # Criação do UserProfileExample associado
            UserProfileExample.objects.create(
                user=novo_user,
                phone_number=serializer.validated_data['telefone'],
                address="",
                birth_date=None
            )

            serializer_saida = MoradorSerializer(novo_morador)
            return Response(
                {"Info": "Morador criado!",
                 "data": serializer_saida.data},
                status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {"Info": "Falha ao tentar cadastrar o morador!"},
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
    def buscar_morador(self, request: Request) -> Response:
        """Ação para buscar um morador pelo nome."""
        try:

            nome = request.query_params.get('nome', None)

            if nome:
                moradores = Morador.objects.filter(nome__icontains=nome)
                serializer = MoradorSerializer(moradores, many=True)

                return Response(
                    {"Info": "Moradores encontrados",
                     "data": serializer.data},
                    status=status.HTTP_200_OK)

            else:
                return Response(
                    {"Info": "Parâmetro 'nome' não fornecido!"},
                    status=status.HTTP_400_BAD_REQUEST)

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
    def deletar_morador(self, request: Request) -> Response:
        """Ação para deletar um morador pelo ID."""
        morador_id = request.query_params.get('id', None)

        if morador_id is not None:
            try:
                morador = Morador.objects.get(id=morador_id)
                morador.user.delete()
                morador.delete()

                return Response(
                    {"Info": "Morador deletado com sucesso!"},
                    status=status.HTTP_204_NO_CONTENT)

            except Morador.DoesNotExist:
                return Response(
                    {"Info": "Morador não encontrado!"},
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
                {"Info": "ID do morador não fornecido!"},
                status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path="listar")
    def listar_moradores(self) -> Response:
        """Ação para listar todos os moradores."""

        try:

            moradores = Morador.objects.all()
            serializer = MoradorSerializer(moradores, many=True)

            return Response(
                {"Info": "Lista de Moradores",
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

    @action(methods=['put'], detail=True, url_path="atualizar")
    def atualizar_morador(self, request: Request) -> Response:
        """Ação para atualizar os dados do morador."""

        try:

            morador = self.get_object()
            serializer = MoradorSerializer(
                morador,
                data=request.data,
                partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"Info": "Morador atualizado!",
                     "data": serializer.data},
                    status=status.HTTP_200_OK)

            return Response(
                {"Info": "Erro ao atualizar morador!",
                 "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)

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
