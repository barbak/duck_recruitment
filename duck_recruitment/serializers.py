from django_apogee.models import Etape
from rest_framework import serializers
from .models import CCOURS_Individu, Agent, Ec, EtapeVet, AllEcAnnuel, EtatHeure


class CCOURS_IndividuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCOURS_Individu


class AllEcAnnuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllEcAnnuel

class EtatHeureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatHeure



class AgentSerializer(serializers.ModelSerializer):
    annee = serializers.CharField(max_length=4, source='get_annee', required=False)

    def get_annee(self):
        return ''

    def create(self, validated_data):
        print validated_data.keys()
        annee = None
        if 'get_annee' in validated_data.keys():
            annee = validated_data['get_annee']
            del validated_data['get_annee']
        agent = Agent.objects.get_or_create(**validated_data)[0]
        if annee:
            AllEcAnnuel.objects.get_or_create(agent=agent, annee=annee)
        return agent

    class Meta:
        model = Agent


class EcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ec


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeVet

# class BaseIndividuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BaseIndividu