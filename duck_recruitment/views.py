# coding=utf-8
from __future__ import unicode_literals
from datetime import date, datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import Workbook
from rest_framework import filters
from rest_framework import views
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from duck_recruitment.filters import EcFilter, CcourIndividuFilter, EtatHeureFilter, TitulaireFilter, InvitationEcFilter
from .models import CCOURS_Individu, Ec, Agent, EtapeVet, EtatHeure, AllEcAnnuel, Titulaire, \
    InvitationEc  # , BaseIndividu
from .serializers import CCOURS_IndividuSerializer, AgentSerializer, EcSerializer, EtapeSerializer, EtatHeureSerializer, \
    AllEcAnnuelSerializer, TitulaireSerializer, InvitationEcSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

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
    queryset = Ec.objects.exclude(type_ec__in=['CSEM', 'SEM', 'CVET', 'VETM', 'BLOC', 'UE', 'PAR'])
    paginate_by = 30
    serializer_class = EcSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EcFilter


class EtapeViewSet(viewsets.ModelViewSet):
    # queryset = EtapeVet.objects.filter(cod_cmp='034')
    serializer_class = EtapeSerializer

    def get_queryset(self):
        # queryset = super(EtapeViewSet, self).get_queryset()
        user = User.objects.get(username=self.request.user.username)
        queryset = EtapeVet.objects.filter(cod_cmp='034', cod_etp__cod_etp__in=user.settings_user.etapes.values_list('cod_etp', flat=True))
        return queryset


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


class InvitationEcViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationEcSerializer
    queryset = InvitationEc.objects.all()
    filter_class = InvitationEcFilter
    filter_backends = (filters.DjangoFilterBackend,)


class ConfirmeInvitation(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, *args, **kwargs):
        data = request.data
        invitation = InvitationEc.objects.get(id=data['id'])
        agent = Agent.objects.get_or_create(individu_id=data['numero'])[0]
        allEc = AllEcAnnuel.objects.get_or_create(agent=agent, annee=invitation.annee)[0]
        e = EtatHeure.objects.get_or_create(all_ec_annuel=allEc, ec=invitation.ec)[0]
        e.valider = True
        e.forfaitaire = invitation.forfaitaire
        e.nombre_heure_estime = e.nombre_heure_estime
        e.save()
        invitation.date_acceptation = date.today()
        invitation.numero = data['numero']
        invitation.save()
        return Response(InvitationEcSerializer(invitation).data)


### SUMMARY VIEW ###

# def convert_etat_heure_to_summary_line_dict(etat_heure):
#     return {
#         'etape': etat_heure.ec.etape.all()[0].cod_etp.cod_etp.encode("ascii", "ignore"),
#         'libelle_etape': etat_heure.ec.etape.all()[0].cod_etp.lib_etp.encode("ascii", "ignore"),
#         'ec': etat_heure.ec.code_ec.encode("ascii", "ignore"),
#         'libelle_ec': etat_heure.ec.lib_ec.encode("ascii", "ignore"),
#         'nom': etat_heure.all_ec_annuel.agent.last_name.encode("ascii", "ignore"),
#         'prenom': etat_heure.all_ec_annuel.agent.first_name1.encode("ascii", "ignore"),
#         'tit': etat_heure.all_ec_annuel.agent.type.encode("ascii", "ignore"),
#         'email': etat_heure.all_ec_annuel.agent.email.encode("ascii", "ignore"),
#     }

def convert_etat_heure_to_summary_line_dict(etat_heure):
    return {
        'etape': etat_heure.ec.etape.all()[0].cod_etp.cod_etp,
        'libelle_etape': etat_heure.ec.etape.all()[0].cod_etp.lib_etp,
        'ec': etat_heure.ec.code_ec,
        'libelle_ec': etat_heure.ec.lib_ec,
        'nom': etat_heure.all_ec_annuel.agent.last_name,
        'prenom': etat_heure.all_ec_annuel.agent.first_name1,
        'tit': etat_heure.all_ec_annuel.agent.type,
        'email': etat_heure.all_ec_annuel.agent.email,
    }


def summary_lines_to_csv(summary_lines):
    csv_str = ""
    for l in summary_lines:
        csv_str += "{};{};{};{};{};{};{};{}\n".format(l['etape'].encode("ascii", "ignore"), l['libelle_etape'].encode("ascii", "ignore"),
                                                   l['ec'].encode("ascii", "ignore"), l['libelle_ec'].encode("ascii", "ignore"),
                                                   l['nom'].encode("ascii", "ignore"), l['prenom'].encode("ascii", "ignore"),
                                                   l['tit'].encode("ascii", "ignore"), l['email'].encode("ascii", "ignore"))
    return csv_str

def summary_lines_to_xls(summary_lines):
    wb = Workbook()
    ws = wb.active
    for l in summary_lines:
        ws.append([l['etape'], l['libelle_etape'], l['ec'], l['libelle_ec'],
                   l['nom'], l['prenom'], l['tit'], l['email']])
    return wb


class SummaryView(View):
    def get(self, request):
        format_type = request.GET.get('type', 'csv') # csv or xls
        etp_name = request.GET.get('etape')
        ec_name = request.GET.get('ec')
        vrs_vet_name = request.GET.get('vrs_vet')
        summary_lines = []

        if not ec_name and not etp_name:
            for eh  in EtatHeure.objects.all():
                summary_lines.append(convert_etat_heure_to_summary_line_dict(eh))

        if ec_name:
            ec = Ec.objects.get(pk=ec_name)
            for eh  in EtatHeure.objects.filter(ec=ec):
                summary_lines.append(convert_etat_heure_to_summary_line_dict(eh))

        if etp_name:
            for eh  in EtatHeure.objects.filter(ec__etape__cod_etp__cod_etp__in=[etp_name],
                                                ec__etape__cod_vrs_vet__in=[510, 520]):
                summary_lines.append(convert_etat_heure_to_summary_line_dict(eh))

        if format_type == 'csv':
            response = HttpResponse(summary_lines_to_csv(summary_lines),
                                    content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=summary_recruitment_{}.csv'\
                    .format(datetime.today().strftime('%d-%m-%Y'))

            return response

        elif format_type == 'xls':
            response = HttpResponse(save_virtual_workbook(summary_lines_to_xls(summary_lines)),
                                    content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=summary_recruitment_{}.xlsx'\
                    .format(datetime.today().strftime('%d-%m-%Y'))
            return response

        else:
            raise NotImplementedError('')

### / SUMMARY VIEW ###
