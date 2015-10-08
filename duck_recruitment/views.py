# coding=utf-8
from __future__ import unicode_literals
from django.views.generic import TemplateView
from rest_framework import filters
from rest_framework import viewsets
from duck_recruitment.filters import EcFilter, CcourIndividuFilter, EtatHeureFilter, TitulaireFilter
from .models import CCOURS_Individu, Ec, Agent, EtapeVet, EtatHeure, AllEcAnnuel, Titulaire  # , BaseIndividu
from .serializers import CCOURS_IndividuSerializer, AgentSerializer, EcSerializer, EtapeSerializer, EtatHeureSerializer, \
    AllEcAnnuelSerializer, TitulaireSerializer


class DeclareAgentView(TemplateView):
    template_name = "duck_recruitment/declare_agent.html"
    # En faire un adminx.views.Dashboard ???


class CCOURS_IndividuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CCOURS_Individu.objects.using('ccours').all()
    serializer_class = CCOURS_IndividuSerializer
    lookup_field = 'numero'
    paginate_by = 30
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CcourIndividuFilter

    def list(self, request, *args, **kwargs):

        data_c = self.get_result(CCOURS_Individu.objects.using('ccours').all(), CcourIndividuFilter, CCOURS_IndividuSerializer)
        data_tit = self.get_result(Titulaire.objects.all(), TitulaireFilter, TitulaireSerializer)

        return self.get_paginated_response(data_c+data_tit)

    def get_result(self, queryset, filter_class, serializer_class):
        self.filter_class = filter_class
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return serializer.data

        serializer = serializer_class(queryset, many=True)
        return serializer.data


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
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EtatHeureFilter


class AllEcAnnuelViewSet(viewsets.ModelViewSet):
    queryset = AllEcAnnuel.objects.all()
    serializer_class = AllEcAnnuelSerializer


class TitulaireViewSet(viewsets.ModelViewSet):
    serializer_class = TitulaireSerializer
    queryset = Titulaire.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TitulaireFilter
