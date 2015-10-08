from django_apogee.models import Etape
from rest_framework import serializers
from .models import CCOURS_Individu, Agent, Ec, EtapeVet, AllEcAnnuel, EtatHeure, Titulaire


class CCOURS_IndividuSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'charge'

    class Meta:
        model = CCOURS_Individu


class TitulaireSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'tit'

    class Meta:
        model = Titulaire


class AllEcAnnuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllEcAnnuel


class EtatHeureSerializer(serializers.ModelSerializer):
    info_perso = serializers.SerializerMethodField()

    def get_info_perso(self, obj):
        return '{} {}'.format(obj.all_ec_annuel.agent.last_name, obj.all_ec_annuel.agent.first_name)

    class Meta:
        model = EtatHeure


class AgentSerializer(serializers.ModelSerializer):
    annee = serializers.CharField(max_length=4, source='get_annee', required=False)
    code_ec = serializers.CharField(max_length=15, source='get_ec', required=False)

    def get_annee(self):
        return ''

    def get_ec(self):
        return ''

    def create(self, validated_data):
        annee = None
        ec = None
        if 'get_annee' in validated_data.keys():
            annee = validated_data['get_annee']
            del validated_data['get_annee']
        if 'get_ec' in validated_data.keys():
            ec = validated_data['get_ec']
            del validated_data['get_ec']

        agent = Agent.objects.get_or_create(**validated_data)[0]
        if annee:
            allEc = AllEcAnnuel.objects.get_or_create(agent=agent, annee=annee)[0]
        if annee and ec:
            ec = Ec.objects.get(code_ec=ec)
            EtatHeure.objects.get_or_create(all_ec_annuel=allEc, ec=ec)
        return agent

    class Meta:
        model = Agent


class EcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ec


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeVet