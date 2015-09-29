import json
import datetime
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CCOURS_Individu, Agent# , BaseIndividu
from .serializers import CCOURS_IndividuSerializer, AgentSerializer #, BaseIndividuSerializer

class DeclareAgentView(TemplateView):
    template_name = "duck_recruitment/declare_agent.html"
    # En faire un adminx.views.Dashboard ???


class CCOURS_IndividuViewSet(viewsets.ModelViewSet):
    queryset = CCOURS_Individu.objects.using('ccours').all()
    serializer_class = CCOURS_IndividuSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    def get_queryset(self):
        pk = self.request.query_params.get('pk', None)
        if pk:
            return self.queryset.filter(pk=pk)

        return self.queryset

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
