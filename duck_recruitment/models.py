# -*- coding: utf8 -*-
from django.db import models


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

# class BaseIndividu(models.Model):
#     """
#     Implementation interne d'un individu dans l'application.
#     """
#     GENDER_CHOICES = (
#         ('M', 'Homme'), ('F', 'Femme'), ('?', 'Non communiqué')
#     )
#     last_name = models.CharField(u"Nom patronymique", max_length=30, null=True)
#     common_name = models.CharField(u"Nom d'époux", max_length=30, null=True, blank=True)
#     first_name1 = models.CharField(u"Prénom", max_length=30)
#     first_name2 = models.CharField(u"Deuxième prénom", max_length=30, null=True, blank=True)
#     first_name3 = models.CharField(u"Troisième prénom", max_length=30, null=True, blank=True)
#     personal_email = models.EmailField("Email", unique=True, null=True)
#     date_registration_current_year = models.DateTimeField(auto_now_add=True)
#     sex = models.CharField(u'sexe', max_length=1, choices=GENDER_CHOICES, null=True)
#     birthday = models.DateField('date de naissance', null=True)
#     #category = models.ForeignKey(CategoriePersonne, null=True, blank=True)
#
# class Agent(models.Model):
#     # Django can;t have a foreign key accross several dbs
#     # https://docs.djangoproject.com/en/1.8/topics/db/multi-db/#limitations-of-multiple-databases
#     # ccours_ind = models.ForeignKey(CCOURS_Individu, null=True)
#     ccours_ind = models.IntegerField(null=True)
#     int_ind = models.ForeignKey(BaseIndividu, null=True)
#
#     def family_name(self):
#         """
#         last name (en), nom patronymique (fr)
#         """
#         if self.ccours_ind:
#             return self.ccours_ind.nom_pat
#
#         return self.int_ind.last_name
#
#     def use_name(self):
#         """
#         use name (en), nom d'usage (fr)
#         """
#         if self.ccours_ind:
#             return self.ccours_ind.nom_usuel
#
#         return self.int_ind.common_name
#
#     def first_name(self):
#         """
#         first name (en), prénom (fr)
#         """
#         if self.ccours_ind:
#             return self.ccours_ind.prenom
#
#         return self.int_ind.first_name1
#
#     def first_names(self):
#         """
#         first names (en), prénoms (fr)
#         """
#         if self.ccours_ind:
#             return [self.ccours_ind]
#
#         first_names = [self.int_ind.first_name1]
#         if self.int_ind.first_name2:
#             first_names.append(self.int_ind.first_name2)
#
#         if self.int_ind.first_name3:
#             first_names.append(self.int_ind.first_name3)
#
#         return first_names

class Agent(models.Model):

    ccours_ref_id = models.IntegerField(null=True)
    GENDER_CHOICES = (
        ('M', 'Homme'), ('F', 'Femme')
    )
    last_name = models.CharField(u"Nom patronymique", max_length=30, null=True)
    common_name = models.CharField(u"Nom d'époux", max_length=30, null=True, blank=True)
    first_name1 = models.CharField(u"Prénom", max_length=30)
    first_name2 = models.CharField(u"Deuxième prénom", max_length=30, null=True, blank=True)
    first_name3 = models.CharField(u"Troisième prénom", max_length=30, null=True, blank=True)
    personal_email = models.EmailField("Email", unique=True, null=True)
    #?? date_registration_current_year = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(u'sexe', max_length=1, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField('date de naissance', null=True)
    #category = models.ForeignKey(CategoriePersonne, null=True, blank=True)

    # Clean API
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



class EC(models.Model):
    code = models.CharField(max_length=8)
    label = models.CharField(max_length=128)
    description = models.TextField()