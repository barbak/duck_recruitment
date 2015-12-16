# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from duck_recruitment.models import EtatHeure, EtapeVet, Ec


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
    type = models.CharField(choices=(('0', 'Annuel'), ('1', 'Premier semestre'), ('2', 'Seconde semestre')),
                            default='0', max_length=1)
    annee = models.IntegerField(default=2015)
    ec = models.ForeignKey(Ec)

    class Meta:
        app_label = "jeton"

    def __str__(self):
        return u"%s %s" % (self.ec, self.annee)
