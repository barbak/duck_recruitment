# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from duck_recruitment.models import EtatHeure, EtapeVet, Ec


@python_2_unicode_compatible
class TypeEc(models.Model):
    label = models.CharField(max_length=60)
    etape = models.ForeignKey(EtapeVet)

    def __str__(self):
        return u"%s %s" % (self.label, self.etape.cod_etp)


@python_2_unicode_compatible
class TypeEtatHeure(models.Model):
    code = models.CharField(primary_key=True, max_length=5)
    label = models.CharField(u"Label", max_length=30)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class TypeActe(models.Model):
    label = models.CharField(max_length=60)
    type_forfait = models.BooleanField(default=False)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class HeureForfait(models.Model):
    type_ec = models.ForeignKey(TypeEc)
    etape = models.ForeignKey(EtapeVet)
    value = models.FloatField()
    annee = models.IntegerField(default=2015)
    semestriel = models.BooleanField(default=False)
    proratise = models.BooleanField(u"Fixe", default=True)

    def __str__(self):
        return u"%s %s" % (self.type_ec, self.value)


@python_2_unicode_compatible
class HorsForfait(models.Model):
    type_acte = models.ForeignKey(TypeActe)
    etape = models.ForeignKey(EtapeVet)
    value = models.FloatField()
    annee = models.IntegerField(default=2015)
    extra = 1

    def __str__(self):
        return u"%s %s" % (self.type_acte, self.value)


@python_2_unicode_compatible
class Forfait(models.Model):
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
