# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_apogee.models import Etape
from duck_recruitment.managers import EcManager
from django.conf import settings
from mailrobot.models import Mail

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


@python_2_unicode_compatible
class Titulaire(models.Model):
    numero = models.IntegerField(null=True, blank=True)
    nom_pat = models.CharField(max_length=100, null=True)
    nom_usuel = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True)
    dnaissance = models.DateField(null=True, blank=True)
    mail = models.CharField(max_length=254, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            self.numero = self.pk
        super(Titulaire, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '{} {}'.format(self.nom_pat, self.prenom)

    class Meta:
        ordering = ['nom_pat']


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



    @property
    def family_name(self):
        """
        (en), nom patronymique (fr)
        """
        return self.last_name

    @property
    def use_name(self):
        """
        use name (en), nom d'usage (fr)
        """
        return self.common_name

    @property
    def first_name(self):
        """
        first name (en), prénom (fr)
        """
        return self.first_name1

    @property
    def first_names(self):
        """
        first names (en), prénoms (fr)
        """
        first_names = [self.first_name1]
        if self.first_name2:
            first_names.append(self.first_name2)

        if self.first_name3:
            first_names.append(self.first_name3)

        return first_names

    @property
    def email(self):
        return self.personal_email


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
    date_creation = models.DateField(auto_now_add=True)


class EtatHeure(models.Model):
    all_ec_annuel = models.ForeignKey(AllEcAnnuel)
    ec = models.ForeignKey(Ec)
    forfaitaire = models.BooleanField(default=True)
    nombre_heure_estime = models.FloatField(null=True, blank=True)
    valider = models.BooleanField(default=False)
    date_creation = models.DateField(auto_now_add=True)

    def envoi_mail_information(self):
        recipients = [self.all_ec_annuel.agent.email if not settings.DEBUG else 'paul.guichon@gmail.com']
        context = {
            'agent': self.all_ec_annuel.agent,
            'ec': self
        }
        if self.all_ec_annuel.agent.type == 'tit':
            template = Mail.objects.get(name='invitation_titulaire')

        else:
            template = Mail.objects.get(name='invitation_charge')
        mail = template.make_message(recipients=recipients, context=context)
        mail.send()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            etat = EtatHeure.objects.get(pk=self.pk)
            if self.valider and not etat.valider:
                self.envoi_mail_information()
        super(EtatHeure, self).save(force_insert, force_update, using, update_fields)


class InvitationEc(models.Model):
    annee = models.CharField(max_length=4, default='2015')
    ec = models.ForeignKey(Ec)
    email = models.EmailField()
    valider = models.BooleanField(default=False)
    numero = models.IntegerField(null=True)
    date_creation = models.DateField(auto_now_add=True)
    date_acceptation = models.DateField(null=True)
    forfaitaire = models.BooleanField(default=True)
    nombre_heure_estime = models.FloatField(null=True, blank=True)

    def envoi_mail_information(self):
        recipients = [self.email if not settings.DEBUG else 'paul.guichon@iedparis8.net']
        context = {
                'invitation': self,
            }

        template = Mail.objects.get(name='invitation_inconnu')
        mail = template.make_message(recipients=recipients, context=context)
        mail.send()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk:
            etat = InvitationEc.objects.get(pk=self.pk)
            if self.valider and not etat.valider:
                self.envoi_mail_information()
        super(InvitationEc, self).save(force_insert, force_update, using, update_fields)

###
#  lien pour les etapes des comptes de prof, il faut le remplacer par un systeme de permission générique
#  c'est uniquement créer pour inviter une dépendance à duck_inscription
###


class SettingsEtapes(Etape):
    class Meta:
        db_table = 'duck_inscription_settingsetape'
        managed = False


class SettingsUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='settings_user')
    etapes = models.ManyToManyField(SettingsEtapes, related_name='etapes_settings', through='SettingsEtapeUser')

    class Meta:
        db_table = 'duck_inscription_settingsuser'
        managed = False


class SettingsEtapeUser(models.Model):
    settings_user = models.ForeignKey(SettingsUser, db_column='settingsuser_id')
    settings_etape = models.ForeignKey(SettingsEtapes, db_column='settingsetape_id')

    class Meta:
        db_table = 'duck_inscription_settingsuser_etapes'
        managed = False

###
#  fin de la merde pondu
###