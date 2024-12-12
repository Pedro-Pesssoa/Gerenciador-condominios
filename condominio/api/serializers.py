from rest_framework.serializers import ModelSerializer

from condominio.models import CondominioModel, CasaModel


class CasaSerializer(ModelSerializer):

    class Meta:
        model = CasaModel
        fields = "__all__"


class CondominioSerializer(ModelSerializer):

    class Meta:
        model = CondominioModel
        fields = "__all__"
