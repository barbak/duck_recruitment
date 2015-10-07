# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_apogee.models import InsAdmEtp, Individu, Adresse, AnneeUni, ConfAnneeUni, EtpGererCge, InsAdmEtpInitial, \
    Etape

from duck_recruitment.models import Ec, EtapeVet

__author__ = 'paul'
from django.core.management.base import BaseCommand
from optparse import make_option
from django.db import connections

QUERY_ETAPE = """SELECT COD_ETP, COD_VRS_VET, COD_CMP FROM VERSION_ETAPE WHERE COD_CMP='034';"""

QUERY_EC = """SELECT LPAD('',(NVL(LEVEL,0) - 1 ) ) || ere.COD_ELP_FILS "code_ec_id", ere.cod_elp_fils "id"
, elp.cod_nel "type_ec" , elp.lib_elp "lib_ec", elp.tem_sca_elp "tem_sec", ere.cod_elp_pere "code_elp_pere",
ere.cod_lse "code_lse"
FROM ELP_REGROUPE_ELP ERE,
element_pedagogi elp,
composante cmp
where
ere.COD_ELP_FILS = elp.COD_ELP
and elp.COD_CMP = cmp.cod_cmp
START WITH ERE.COD_LSE IN
(SELECT LSE.COD_LSE
FROM LISTE_ELP LSE,VET_REGROUPE_LSE VRL
WHERE
LSE.COD_LSE = VRL.COD_LSE
AND VRL.COD_ETP = %s
AND VRL.COD_VRS_VET = %s
AND VRL.DAT_FRM_REL_LSE_VET IS NULL
AND LSE.ETA_LSE != 'F' )
AND ERE.COD_ELP_PERE IS NULL
AND ERE.ETA_ELP_FILS != 'F' AND ERE.TEM_SUS_ELP_FILS = 'N'
CONNECT BY PRIOR ERE.COD_ELP_FILS = ERE.COD_ELP_PERE
AND ERE.ETA_ELP_FILS != 'F' AND ERE.TEM_SUS_ELP_FILS = 'N'
AND NVL(ERE.ETA_ELP_PERE,'O') != 'F'
AND NVL(ERE.TEM_SUS_ELP_PERE,'N') = 'N'
AND ERE.ETA_LSE != 'F' AND DATE_FERMETURE_LIEN IS NULL;"""

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--annee',
                    action='store',
                    type="int",
                    dest='annee',
                    default=None,
                    help='annee de remontee'),
    )
    def init_etape(self):
        cursor = connections['oracle'].cursor()
        cursor.execute(QUERY_ETAPE)
        for etape in cursor.fetchall():
            e = Etape.objects.using('oracle').get(cod_etp=etape[0])
            e.save(using='default')
            EtapeVet.objects.get_or_create(cod_etp_id=etape[0], cod_vrs_vet=etape[1], cod_cmp=etape[2])
        print EtapeVet.objects.count()

    def init_ec(self):
        code_ec_id = 0
        type_ec = 2
        lib_ec = 3
        tem_sec = 4

        cursor = connections['oracle'].cursor()
        etps = EtapeVet.objects.filter(cod_cmp='034')
        for x in etps:
            cursor.execute(QUERY_EC, [x.cod_etp.cod_etp, x.cod_vrs_vet])
            print x.cod_etp.cod_etp, x.cod_vrs_vet
            for ec in cursor.fetchall():
                a = Ec.objects.get_or_create(code_ec=ec[code_ec_id], id=ec[code_ec_id])[0]
                a.lib_ec = ec[lib_ec]
                a.tem_sec = ec[tem_sec]
                a.type_ec = ec[type_ec]
                a.save(using='default')
                a.etape.add(x)

    def handle(self, *args, **options):
        # self.init_etape()
        self.init_ec()
