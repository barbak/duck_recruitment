# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django_apogee.models import Etape
from duck_recruitment.managers import EcManager
from django.conf import settings
from mailrobot.models import Mail


@python_2_unicode_compatible
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

    def __str__(self):
        return "{} {}" .format(self.nom_pat, self.prenom)

    class Meta:
        managed = False
        db_table = 'INDIVIDU'
        app_label = "duck_recruitment"


@python_2_unicode_compatible
class TypeAdresse(models.Model):
    id = models.IntegerField(primary_key=True, db_column='TYPA_ID')
    libelle = models.CharField(max_length=2000, null=True, db_column='TYPA_ADRESSE')

    def __str__(self):
        return self.libelle

    class Meta:
        managed = False
        db_table = 'TYPE_ADRESSE'
        app_label = "duck_recruitment"


@python_2_unicode_compatible
class AdresseCcours(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ADR_ID')
    cp = models.CharField(max_length=5, null=True, blank=True, db_column='ADR_CP')
    insee = models.CharField(max_length=5, null=True, blank=True, db_column='ADR_INSEE')
    adresse = models.CharField(max_length=2000, null=True, blank=True, db_column='ADR_ADRESSE')
    type_adresse = models.ForeignKey(TypeAdresse, null=True, db_column='TYPA_ID')
    adresse_suite = models.CharField(max_length=2000, null=True, db_column='ADR_ADRESSE_SUITE')
    commune = models.CharField(max_length=2000, null=True, db_column='ADR_COMMUNE')
    pays = models.CharField(max_length=3, null=True, db_column='ADR_PAYS')
    port = models.CharField('telephone portable', max_length=2000, null=True, db_column='ADR_PORT')
    tel = models.CharField('telephone fixe', max_length=2000, null=True, db_column='ADR_TEL')
    voie = models.CharField(max_length=50, null=True, db_column='ADR_VOIE')
    individu = models.ForeignKey(CCOURS_Individu, null=True, db_column='INDIV_ID', related_name='adresses')

    def __str__(self):
        return self.adresse

    class Meta:
        managed = False
        db_table = 'ADRESSE'
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


@python_2_unicode_compatible
class Agent(models.Model):

    individu_id = models.IntegerField(null=True)
    type = models.CharField(choices=(('charge', 'Chargé de cours'), ('tit', 'Titulaire')), max_length=10, null=True)

    GENDER_CHOICES = (
        ('M', 'Homme'), ('F', 'Femme')
    )
    last_name = models.CharField(u"Nom patronymique", max_length=100, null=True)
    common_name = models.CharField(u"Nom d'époux", max_length=100, null=True, blank=True)
    first_name1 = models.CharField(u"Prénom", max_length=100, null=True)
    personal_email = models.EmailField("Email", unique=True, null=True)
    birthday = models.DateField('date de naissance', null=True)

    @property
    def adresses(self):
        if self.type == 'tit':
            return None
        individu = CCOURS_Individu.objects.using('ccours').get(numero=self.individu_id)
        return individu.adresses.all()

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name1)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        force_insert = False
        self.id = self.individu_id
        if self.type == 'charge':
            self._copy_dsi()
        else:
            self._copy_tit()
        try:
            super(Agent, self).save(force_insert, force_update, using, update_fields)
        except IntegrityError:
            super(Agent, self).save(force_insert, True, using, update_fields)

    def _copy_tit(self):
        ind = Titulaire.objects.get(numero=self.individu_id)
        self._copy_ind(ind)

    def _copy_dsi(self):
        ind = CCOURS_Individu.objects.using('ccours').get(numero=self.individu_id)
        self._copy_ind(ind)

    def _copy_ind(self, ind):
        try:
            a = Agent.objects.get(personal_email=ind.mail)
            self.pk = a.id
        except Agent.DoesNotExist:
            pass
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


@python_2_unicode_compatible
class EtapeVet(models.Model):
    cod_etp = models.ForeignKey(Etape)
    cod_vrs_vet = models.CharField(max_length=3)
    cod_cmp = models.CharField(max_length=3)

    def lib_etp(self):
        return self.cod_etp.lib_etp

    def __str__(self):
        return "{} {}".format(self.cod_etp.cod_etp, self.cod_vrs_vet)


@python_2_unicode_compatible
class Ec(models.Model):
    id = models.CharField('id element', max_length=8, primary_key=True)
    etape = models.ManyToManyField(EtapeVet)
    code_ec = models.CharField('code element', max_length=8, unique=True)
    type_ec = models.CharField('type element', max_length=4)
    lib_ec = models.CharField('libelle', max_length=120)
    tem_sec = models.CharField('tem_sec', max_length=1)
    objects = EcManager()
    type = models.ForeignKey('TypeEc', null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.code_ec, self.lib_ec)


@python_2_unicode_compatible
class AllEcAnnuel(models.Model):
    agent = models.ForeignKey(Agent)
    annee = models.CharField(max_length=4, default='2015')
    date_creation = models.DateField(auto_now_add=True)

    def all_ec_lib(self):
        return ['{} {} {}'.format(ec.ec.code_ec, ec.ec.lib_ec.encode("ascii", "ignore"), ec.etps)
                for ec in self.etatheure_set.all()]

    def __str__(self):
        return "{} {}".format(self.agent_id, self.annee)


@receiver(post_save)
def mise_a_jour_cache_etat_heure(sender, instance, **kwargs):
    if sender == HeureForfait:
        for etat in EtatHeure.objects.filter(ec__type=instance.type_ec, all_ec_annuel__annee=instance.annee):
            etat.calcul_forfait()
    if sender == Ec:
        for etat in instance.etatheure_set.all():
            etat.calcul_forfait()

@python_2_unicode_compatible
class EtatHeure(models.Model):
    """
    la classe qui permet de faire le lien entre une ec et un agent de façon annualisé
    par le bien de all_ec_annuel (qui est le regoupement de tous les ec de la personne pour une année
    elle doit calculer la proratisation (rattachement), donner le forfait, donner le total du premier semestre
    decomposer en : la partie du forfait du et le hors forfait si nécessaire (les actes pédagogiques en plus de ceux
    définis) et la même chose pour le total de l'année.
    Pour rappel : le rattachement c'est les heures de septembre à décembre
    le premier semestre c'est ce qui est du pour le premier semestre (rattachement compris)
    le total annuel c'est ce qui est du à l'année.
    """

    all_ec_annuel = models.ForeignKey(AllEcAnnuel)
    ec = models.ForeignKey(Ec)
    forfaitaire = models.BooleanField(default=True)
    nombre_heure_estime = models.FloatField(null=True, blank=True)
    valider = models.BooleanField(default=False)
    date_creation = models.DateField(auto_now_add=True)
    _forfait = models.FloatField("cache pour le forfait", null=True, default=None)

    @property
    def ratachement(self):
        """
        la somme du pour la période de septembre à décembre
        :return: le total du
        :rtype: float
        """
        return 0

    @property
    def forfait(self):
        """
        :return: la valeur du forfait (en heure) de l'état heure
        :rtype: float
        """
        if self._forfait is None:
            self.calcul_forfait()
        return self._forfait

    def calcul_forfait(self):

        if not self.forfaitaire:
            self._forfait = 0
        try:
            value = HeureForfait.objects.filter(type_ec=self.ec.type, annee='2015', etape=self.ec.type.etape).values_list('value', flat=True).first()
            self._forfait = value
        except AttributeError:
            self._forfait = None
        self.save()


    @property
    def etps(self):
        return ' '.join([etp.cod_etp.cod_etp for etp in self.ec.etape.all()])

    def envoi_mail_information(self):
        recipients = [self.all_ec_annuel.agent.email if not settings.DEBUG else 'paul.guichon@gmail.com']
        context = {
            'agent': self.all_ec_annuel.agent,
            'ec': self.ec
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

    def __str__(self):
        return "{}".format(self.id)


@python_2_unicode_compatible
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
                'ec': self.ec
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

    def __str__(self):
        return "{} {} {}".format(self.ec.code_ec, self.email, self.annee)


###
#  lien pour les etapes des comptes de prof, il faut le remplacer par un systeme de permission générique
#  c'est uniquement créer pour inviter une dépendance à duck_inscription
###

@python_2_unicode_compatible
class SettingsEtapes(Etape):

    def __str__(self):
        return ""

    class Meta:
        db_table = 'duck_inscription_settingsetape'
        managed = False


@python_2_unicode_compatible
class SettingsUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='settings_user')
    etapes = models.ManyToManyField(SettingsEtapes, related_name='etapes_settings', through='SettingsEtapeUser')

    def __str__(self):
        return ""

    class Meta:
        db_table = 'duck_inscription_settingsuser'
        managed = False


@python_2_unicode_compatible
class SettingsEtapeUser(models.Model):
    settings_user = models.ForeignKey(SettingsUser, db_column='settingsuser_id')
    settings_etape = models.ForeignKey(SettingsEtapes, db_column='settingsetape_id')

    def __str__(self):
        return ""

    class Meta:
        db_table = 'duck_inscription_settingsuser_etapes'
        managed = False


@python_2_unicode_compatible
class TypeEc(models.Model):
    """
    Permet de créer des groupes d'EC d'une étape possédant les mêmes propriétés financières.
    Exemple :
    Ec droit de L1NDRO : groupe Standard
    Ec jurique de L1NDRO : groupe Standard
    forfait, horforfait etc de EC droit = EC juridique
    """
    label = models.CharField(max_length=60)  # validée
    etape = models.ForeignKey(EtapeVet)  # validée

    def __str__(self):
        return u"%s %s" % (self.label, self.etape.cod_etp)


@python_2_unicode_compatible
class TypeEtatHeure(models.Model):
    code = models.CharField(primary_key=True, max_length=5)  # validée
    label = models.CharField(u"Label", max_length=30)  # validée

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class TypeActe(models.Model):
    """
    les types d'actes pédagoqigues disponibles decomposer une activité d'enseignement
    """
    label = models.CharField(max_length=60)  # validée
    type_forfait = models.BooleanField(default=False)  # ???????

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class HeureForfait(models.Model):
    """
    décrit la propriété financière d'un type d'ec pour une étape donnée.
    """

    type_ec = models.ForeignKey(TypeEc)  # validée
    etape = models.ForeignKey(EtapeVet)  # validée
    value = models.FloatField()  # validée
    annee = models.IntegerField(default=2015)  # validée
    semestriel = models.BooleanField(default=False)  # validée TODO voir si ce n'est pas mieux de mettre ce champ ailleurs
    proratise = models.BooleanField(default=True, verbose_name="fixe ")

    def __str__(self):
        return u"%s %s" % (self.type_ec, self.value)


@python_2_unicode_compatible
class HorsForfait(models.Model):
    """
    Permet savoir le tarif des actes qui sont hors forfait.
    """
    type_acte = models.ForeignKey(TypeActe)
    etape = models.ForeignKey(EtapeVet)
    value = models.FloatField()
    annee = models.IntegerField(default=2015)

    def __str__(self):
        return u"%s %s" % (self.type_acte, self.value)


@python_2_unicode_compatible
class Forfait(models.Model):
    """
    Pour un type d'ec, permet de savoir de quel type et le nombre d'unité est composé le forfait du type :
    Exemple : pour le type standart de L1NDRO grace à HeureForfait le forfait vaut 15h.
    Avec Forfait je sais que qu'il y a correction de copie (200 copies soit 5h ) et Cours (10h)

    """
    type_ec = models.ForeignKey(TypeEc)
    type_acte = models.ForeignKey(TypeActe)
    etape = models.ForeignKey(EtapeVet)
    value = models.FloatField()
    annee = models.IntegerField(default=2015)
    extra = 1

    def __str__(self):
        return u"%s %s %s" % (self.type_ec, self.type_acte, self.value)


@python_2_unicode_compatible
class StatutEtatHeure(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    label = models.CharField(max_length=60)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Acte(models.Model):
    etat_heure = models.ForeignKey(EtatHeure)
    type_acte = models.ForeignKey(TypeActe)
    ratrapage = models.FloatField("rattrapage", null=True, blank=True)
    proratisation = models.FloatField("proratisation", null=True, blank=True)
    value_1 = models.FloatField("premier", null=True, blank=True)
    value_2 = models.FloatField("deuxième", null=True, blank=True)
    #cache
    _forfait_value = models.FloatField(null=True, blank=True)
    _hf_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.etat_heure, self.type_acte)


@python_2_unicode_compatible
class PropEc(models.Model):
    """
    propriété de l'ec pour calculer la proratisation et le premier semestre
    """
    type = models.CharField(choices=(('0', 'Annuel'), ('1', 'Premier semestre'), ('2', 'Seconde semestre')),
                            default='0', max_length=1)
    annee = models.IntegerField(default=2015)
    ec = models.ForeignKey(Ec)

    def __str__(self):
        return u"%s %s" % (self.ec, self.annee)

###
#  fin de la merde pondu
###
