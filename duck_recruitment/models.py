# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django_apogee.models import Etape
from duck_recruitment.managers import EcManager


class CCOURS_Individu(models.Model):
    id = models.IntegerField(db_column='INDIV_ID', primary_key=True)
    numero = models.IntegerField(db_column='INDIV_NUMERO')
    civilite = models.CharField(max_length=20, db_column='INDIV_CIVILITE')
    nom_pat = models.CharField(max_length=2000, db_column='INDIV_NOM_PAT')
    nom_usuel = models.CharField(max_length=2000, db_column='INDIV_NOM_USUEL')
    prenom = models.CharField(max_length=2000, db_column='INDIV_PRENOM')
    dnaissance = models.DateField(db_column='INDIV_DNAISSANCE')
    dept_naissa = models.CharField(max_length=3, db_column='INDIV_DEPT_NAISSA')
    ville_naiss = models.CharField(max_length=2000, db_column='INDIV_VILLE_NAISS')
    pays_naiss = models.CharField(max_length=3, db_column='INDIV_PAYS_NAISS', )
    pays_nationalite = models.CharField(max_length=3, db_column='INDIV_PAYS_NATIONALITE', )
    sitfam = models.CharField(max_length=1, db_column='INDIV_SITFAM')
    no_insee = models.CharField(max_length=13, db_column='INDIV_NO_INSEE')
    cle_insee = models.IntegerField(db_column='INDIV_CLE_INSEE')
    mail = models.CharField(db_column='INDIV_MAIL', max_length=2000)
    login = models.CharField(db_column='INDIV_LOGIN', max_length=2000)
    password = models.CharField(db_column='INDIV_PASSWORD', max_length=2000)
    mangue_id = models.IntegerField(db_column='MANGUE_ID')
    etat_id = models.IntegerField(db_column='ETAT_ID')

    def __unicode__(self):
        return "{} {}" .format(self.nom_pat, self.prenom)

    class Meta:
        managed = False
        db_table = 'INDIVIDU'
        app_label = "duck_recruitment"


class Titulaire(models.Model):
    numero = models.IntegerField(null=True, blank=True)
    nom_pat = models.CharField(max_length=100, null=True)
    nom_usuel = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True)
    dnaissance = models.DateField(null=True, blank=True)
    mail = models.CharField(max_length=254, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Titulaire, self).save(force_insert, force_update, using, update_fields)
        self.numero = self.id
        super(Titulaire, self).save(force_insert, force_update, using, update_fields)


class Agent(models.Model):

    individu_id = models.IntegerField(null=True)
    type = models.CharField(choices=(('charge', 'Chargé de cours'), ('tit', 'Titulaire')), max_length=10, null=True)

    GENDER_CHOICES = (
        ('M', 'Homme'), ('F', 'Femme')
    )
    last_name = models.CharField(u"Nom patronymique", max_length=30, null=True)
    common_name = models.CharField(u"Nom d'époux", max_length=30, null=True, blank=True)
    first_name1 = models.CharField(u"Prénom", max_length=30, null=True)
    personal_email = models.EmailField("Email", unique=True, null=True)
    birthday = models.DateField('date de naissance', null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print self.individu_id, self.type
        self.id = self.individu_id
        if self.type == 'charge':
            self._copy_dsi()
        else:
            self._copy_tit()
        super(Agent, self).save(force_insert, force_update, using, update_fields)

    def _copy_tit(self):
        ind = Titulaire.objects.get(numero=self.individu_id)
        self._copy_ind(ind)

    def _copy_dsi(self):
        ind = CCOURS_Individu.objects.using('ccours').get(numero=self.individu_id)
        self._copy_ind(ind)

    def _copy_ind(self, ind):
        self.last_name = ind.nom_pat
        self.common_name = ind.nom_usuel
        self.first_name1 = ind.prenom
        self.personal_email = ind.mail
        self.birthday = ind.dnaissance


class EtapeVet(models.Model):
    cod_etp = models.ForeignKey(Etape)
    cod_vrs_vet = models.CharField(max_length=3)
    cod_cmp = models.CharField(max_length=3)


class Ec(models.Model):
    id = models.CharField('id element', max_length=8, primary_key=True)
    etape = models.ManyToManyField(EtapeVet)
    code_ec = models.CharField('code element', max_length=8, unique=True)
    type_ec = models.CharField('type element', max_length=4)
    lib_ec = models.CharField('libelle', max_length=120)
    tem_sec = models.CharField('tem_sec', max_length=1)
    objects = EcManager()


class AllEcAnnuel(models.Model):
    agent = models.ForeignKey(Agent)
    annee = models.CharField(max_length=4, default='2015')


class EtatHeure(models.Model):
    all_ec_annuel = models.ForeignKey(AllEcAnnuel)
    ec = models.ForeignKey(Ec)
