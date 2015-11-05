# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django_apogee.models import Etape
from rest_framework import serializers
from .models import CCOURS_Individu, Agent, Ec, EtapeVet, AllEcAnnuel, EtatHeure, Titulaire, InvitationEc


class CCOURS_IndividuSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'charge'

    class Meta:
        model = CCOURS_Individu
        exclude = ('password', 'login', 'mangue_id', 'etat_id')


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
    agent_identity = serializers.SerializerMethodField()
    agent_email = serializers.SerializerMethodField()

    def get_info_perso(self, obj):
        return '{} {} {}'.format(obj.all_ec_annuel.agent.last_name, obj.all_ec_annuel.agent.first_name, obj.all_ec_annuel.agent.email.lower())

    def get_agent_identity(self, obj):
        return '{} {}'.format(obj.all_ec_annuel.agent.last_name,
                              obj.all_ec_annuel.agent.first_name)

    def get_agent_email(self, obj):
        return obj.all_ec_annuel.agent.email.lower()

    def create(self, validated_data):
        e = EtatHeure.objects.get_or_create(ec=validated_data['ec'], all_ec_annuel=validated_data['all_ec_annuel'])[0]
        valider = validated_data.get('valider', None)
        if valider:
            e.valider = valider
            e.save()
        return e

    class Meta:
        model = EtatHeure


class AgentSerializer(serializers.ModelSerializer):
    annee = serializers.CharField(max_length=4, source='get_annee', required=False)
    code_ec = serializers.CharField(max_length=15, source='get_ec', required=False)
    forfaitaire = serializers.BooleanField(source='get_forfaitaire', required=False)
    heure = serializers.FloatField(source='get_heure', required=False)

    def get_annee(self):
        return ''

    def get_ec(self):
        return ''

    def get_forfaitaire(self):
        return ''

    def get_heure(self):
        return ''

    def create(self, validated_data):
        annee = None
        ec = None
        arg = {}

        if 'get_annee' in validated_data.keys():
            annee = validated_data['get_annee']
            del validated_data['get_annee']
        if 'get_ec' in validated_data.keys():
            ec = validated_data['get_ec']
            del validated_data['get_ec']
        if 'get_forfaitaire' in validated_data.keys():
            arg['forfaitaire'] = validated_data['get_forfaitaire']
            del validated_data['get_forfaitaire']
        if 'get_heure' in validated_data.keys():
            arg['nombre_heure_estime'] = validated_data['get_heure']
            del validated_data['get_heure']

        agent = Agent.objects.get_or_create(**validated_data)[0]
        if annee:
            arg['all_ec_annuel'] = AllEcAnnuel.objects.get_or_create(agent=agent, annee=annee)[0]
        if annee and ec:
            arg['ec'] = Ec.objects.get(code_ec=ec)
            EtatHeure.objects.get_or_create(**arg)
        return agent

    class Meta:
        model = Agent


class EcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ec


class EtapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeVet
        fields = ('id', 'cod_etp', "cod_vrs_vet", "cod_cmp", "lib_etp")
        read_only_fields = ('lib_etp',)


class UserSerializer(serializers.ModelSerializer):
    """
    pour les user
    """
    class Meta:
        model = User
        fields = ('username', 'is_superuser', 'email', 'groups')

class InvitationEcSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        invitation = InvitationEc.objects.get_or_create(ec=validated_data['ec'], email=validated_data['email'])[0]
        for key in validated_data:
            setattr(invitation, key, validated_data[key])

        invitation.save()
        return invitation

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        query = CCOURS_Individu.objects.using('ccours').filter(mail__iexact = data['email'])
        if len(query):
            ind = query.first()
            agent = Agent.objects.get_or_create(individu_id=ind.numero)[0]
            allEc = AllEcAnnuel.objects.get_or_create(agent=agent, annee=2015)[0]
            e =EtatHeure.objects.get_or_create(all_ec_annuel=allEc, ec=data['ec'])[0]
            e.nombre_heure_estime = data.get('nombre_heure_estime', None)
            e.forfaitaire = data.get('forfaitaire', True)
            e.save()
            raise serializers.ValidationError('Personne existe déjà')
        return data

    class Meta:
        model = InvitationEc