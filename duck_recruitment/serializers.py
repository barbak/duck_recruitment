from rest_framework import serializers
from .models import CCOURS_Individu, Agent#, BaseIndividu

class CCOURS_IndividuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCOURS_Individu


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent


# class BaseIndividuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BaseIndividu