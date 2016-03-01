# coding=utf-8
__author__ = 'paul'
from django.db import models, IntegrityError


class MaquetteManager(models.Manager):

    def save_ec_apogee(self, etape):
        from jeton.models import Ec
        from apogee.models import Etape
        ecs = self.raw(u'''SELECT
LPAD('',(NVL(LEVEL,0) - 1 ) ) || ere.COD_ELP_FILS "code_ec_id", ere.cod_elp_fils "id"
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
and VRL.COD_ETP = %s
AND VRL.DAT_FRM_REL_LSE_VET IS NULL
AND LSE.ETA_LSE != 'F' )
AND ERE.COD_ELP_PERE IS NULL
AND ERE.ETA_ELP_FILS != 'F' AND ERE.TEM_SUS_ELP_FILS = 'N'
CONNECT BY PRIOR ERE.COD_ELP_FILS = ERE.COD_ELP_PERE
AND ERE.ETA_ELP_FILS != 'F' AND ERE.TEM_SUS_ELP_FILS = 'N'
AND NVL(ERE.ETA_ELP_PERE,'O') != 'F'
AND NVL(ERE.TEM_SUS_ELP_PERE,'N') = 'N'
AND ERE.ETA_LSE != 'F' AND DATE_FERMETURE_LIEN IS NULL;''', [etape]).using('oracle')
        etape1 = Etape.objects.get(cod_etp=etape)
        for i, ec in enumerate(ecs):
            # try:

                # a = Ec.objects.using('default').get(code_ec=ec.code_ec_id, id=ec.code_ec_id,)

            a = Ec.objects.get_or_create(code_ec=ec.code_ec_id, id=ec.code_ec_id)[0]
            a.lib_ec = ec.lib_ec
            a.tem_sec = ec.tem_sec
            a.type_ec = ec.type_ec
            a.save(using='default')
            a.etape.add(etape1)


class EcManager(models.Manager):
    def get_query_set(self):
        return super(EcManager, self).get_query_set().exclude(type_ec__in=['VETM'])
        # return super(EcManager, self).get_query_set()
