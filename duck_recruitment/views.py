# coding=utf-8
from __future__ import unicode_literals
import json
import datetime
from django.views.generic import TemplateView
from django.shortcuts import render
from django_apogee.models import EtpGererCge, Etape
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response

from duck_recruitment.filters import EcFilter, CcourIndividuFilter
from .models import CCOURS_Individu, Ec, Agent, EtapeVet, EtatHeure, AllEcAnnuel  # , BaseIndividu
from .serializers import CCOURS_IndividuSerializer, AgentSerializer, EcSerializer, EtapeSerializer, EtatHeureSerializer, \
    AllEcAnnuelSerializer


class DeclareAgentView(TemplateView):
    template_name = "duck_recruitment/declare_agent.html"
    # En faire un adminx.views.Dashboard ???


class CCOURS_IndividuViewSet(viewsets.ModelViewSet):
    queryset = CCOURS_Individu.objects.using('ccours').all()
    serializer_class = CCOURS_IndividuSerializer
    lookup_field = 'numero'
    paginate_by = 20
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CcourIndividuFilter



class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer





class EcViewSet(viewsets.ModelViewSet):
    """
    permet de récupérer les ec
    filter les etapes d'apogee
    """
    queryset = Ec.objects.exclude(type_ec__in=['CSEM', 'SEM', 'CVET', 'VETM', 'BLOC', 'UE'])
    paginate_by = 30
    serializer_class = EcSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EcFilter


class EtapeViewSet(viewsets.ModelViewSet):
    queryset = EtapeVet.objects.filter(cod_cmp='034')
    serializer_class = EtapeSerializer


class EtatHeureViewSet(viewsets.ModelViewSet):
    queryset = EtatHeure.objects.all()
    serializer_class = EtatHeureSerializer


class AllEcAnnuelViewSet(viewsets.ModelViewSet):
    queryset = AllEcAnnuel.objects.all()
    serializer_class = AllEcAnnuelSerializer


# class BaseIndividuViewSet(viewsets.ModelViewSet):
#     queryset = BaseIndividu.objects.all()
#     serializer_class = BaseIndividuSerializer


# @api_view(['GET', 'POST'])
# def hello_world(request):
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})

class AddAssociationView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        print "GET HELLO - ", args, kwargs
        return Response({"message": "Hello, world!"})

    def post(self, request, *args, **kwargs):
        print "POST HELLO - ", args, kwargs
        # email = request.DATA.get('email', None)
        # url = request.DATA.get('url', None)
        # if email and url:
        #     share_url(email, url)
        #     return Response({"success": True})
        # else:
        #     return Response({"success": False})
        try:
            import pprint

            print type(request.body)
            pprint.pprint(json.loads(request.body))

        except e:
            print e

        # print request.DATA
        return Response({"message": "Got some data!", "data": request.DATA})


class AddAgentView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print "BODY: ", request.body
        post_body = json.loads(request.body)
        # if id field is present, the description is from dsi
        if post_body.has_key('id'):
            self.add_from_dsi(post_body)

        else:
            self.add_agent(post_body)

        return Response('')

    def add_from_dsi(self, agent_dict):
        agent = Agent.objects.create(
            ccours_ref_id = agent_dict['id'],
            last_name = agent_dict['nom_pat'],
            common_name = agent_dict['nom_usuel'],
            first_name1 = agent_dict['prenom'],
            personal_email = agent_dict['mail'],
            birthday = datetime.datetime.strptime(agent_dict['dnaissance'], "%Y-%m-%d")
        )
        #TODO Ajout si necessaire de l'association de l'agent avec une EC
        return agent

    def add_agent(self, agent_dict):
        kw = {}
        if agent_dict.has_key('last_name'):
            kw['last_name'] = agent_dict['last_name']

        if agent_dict.has_key('common_name'):
            kw['common_name'] = agent_dict['common_name']

        if agent_dict.has_key('first_name1'):
            kw['first_name1'] = agent_dict['first_name1']

        if agent_dict.has_key('first_name2'):
            kw['first_name2'] = agent_dict['first_name2']

        if agent_dict.has_key('first_name3'):
            kw['first_name3'] = agent_dict['first_name3']

        if agent_dict.has_key('personal_email'):
            kw['personal_email'] = agent_dict['personal_email']

        if agent_dict.has_key('sex'):
            kw['sex'] = agent_dict['sex']

        if agent_dict.has_key('birthday'):
            kw['birthday'] = datetime.datetime.strptime(agent_dict['birthday'], "%d/%m/%Y")

        agent = Agent.objects.create(**kw)
        #TODO Ajout si necessaire de l'association de l'agent avec une EC
        return agent

class DeleteAgentView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        agent_id = self.request.query_params['pk']
        agent = Agent.objects.get(pk=agent_id)
        # TODO effacer les associations avec les ECs
        agent.delete()
        return Response()

class ModifyAgentView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        agent_dict = json.loads(request.body)
        Agent.objects.update(**agent_dict)
        return Response()
