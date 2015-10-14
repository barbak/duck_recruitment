# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_apogee.models import InsAdmEtp, Individu, Adresse, AnneeUni, ConfAnneeUni, EtpGererCge, InsAdmEtpInitial, \
    Etape

from duck_recruitment.models import Ec, EtapeVet, Titulaire
import json
__author__ = 'paul'
j= """[["BRIDOU", "Morgiane", "", "morgiane.bridou@iedparis8.net"], ["Arnaud", "Plagnol", "", "arnaud.plagnol@iedparis8.net"], ["Lionel", "Dagot", null, "lionel.dagot@iedparis8.net"], ["AMORIM", "Marilia", "DUFOUR", "mamorim@univ-paris8.fr"], ["Antoine", "Corinne", "", "corinne.antoine@iedparis8.net"], ["Baque", "Dominique", "", "dominique.baque@iedparis8.net"], ["Meunier", "Jean-Marc", "", "jean-marc.meunier@iedparis8.net"], ["Bardin", "Brigitte", "", "brigitte.bardin@univ-tlse2.fr"], ["Behra", "Timoth\\u00e9e", "", "timotheebehra.etu@gmail.com"], ["Bernard", "Gilles", "", "gilles.bernard@iedparis8.net"], ["COLIN", "Lucette", "", "lucettecolin@noos.fr"], ["CONTY", "LAurence", "Conty", "laurence.conty@gmail.com"], ["Chicharro", "Gladys", "", "gladyschicharro@hotmail.com"], ["DEBORDE", "Anne-Sophie", "", "anne-spohie.deborde@iedparis8.net"], ["DEMARCHI", "SAMUEL", "", "samuel.demarchi@univ-paris8.fr"], ["DUPUCH", "LAURENCE", "", "laurence.dupuch02@univ-paris8.fr"], ["DURIEZ", "NATHALIE", "TIQUET", "nathalie.duriez-tiquet@univ-paris8.fr"], ["DURIEZ", "NATHALIE", "TIQUET", "nathalie.duriez@iedparis8.net"], ["Dominique", "Baqu\\u00e9", null, "dombaque@orange.fr"], ["ELOY", "Florence", "", "florence_eloy@yahoo.fr"], ["Eriksen", "Anna", "Terzian", "anna.terzian@univ-paris8.fr"], ["Francoise", "Morange-Majoux", "Majoux", "francoise.morange-majoux@iedparis8.net"], ["GUENIF", "NACIRA", "SOUILAMAS", "nacira.guenif@univ-paris8.fr"], ["GUERAUD", "SABINE", "", "sabine.gueraud@univ-paris8.fr"], ["HENNION", "PATRICIA", "JACQUET", "patricia.hennion-jacquet@iedparis8.net"], ["HESS", "Remi", "", "remihess@noos.fr"], ["HOUILLON", "Jean-Charles", "", "jean-charles.houillon@iedparis8.net"], ["Habib", "Marianne", "", "marianne.habib@univ-paris8.fr"], ["Jean", "Laingui", null, "jean.laingui@iedparis8.net"], ["Juhan", "Michel", "", "michel.juhan@univ-paris8.fr"], ["LEFEVRE", "CAROLE", "", "carole.lefevre@iedparis8.net"], ["Laurent", "Jean-Paul", "", "jean-paul.laurent@iedparis8.net"], ["Lesourd", "Francis", "", "francis.lesourd@iedparis8.net"], ["Lujan", "Cristianh", "", "christian.lujan@iedparis8.net"], ["MARIAGE", "Jean-Jacques", "", "jjmariage@free.fr"], ["MASSE", "LAURENCE", "", "laurence.masse@iedparis8.net"], ["Gautier", "Agn\\u00e8s", "Gautier-Audebert", "agnes.gautier.audebert@neuf.fr"], ["MOREAU", "Didier", "", "didier.moreauparis8@gmail.com"], ["Marquez-D.", "Eduardo", "", "eduardo.marquez@iedparis8.net"], ["Mehat", "Jean", "", "jmehat@gmail.com"], ["Monica", "Macedo", "", "monica.macedo@iedparis8.net"], ["Morisse", "Martine", "", "martine.morisse@iedparis8.net"], ["Morisse", "Martine", "", "martine.morisse@univ-paris8.fr"], ["NIVARD", "Jacqueline", "BIGOURDAN", "jacqueline.nivard@iedparis8.net"], ["PAPPA", "ANNA", "", "ap@ai.univ-paris8.fr"], ["Perrotin", "Marie-Liesse", "", "marie-liesse.perrotin@iedparis8.net"], ["STILGENBAUER", "Jean-Louis", "", "jean-louis.stilgenbauer@iedparis8.net"], ["Villemonteix", "Thomas", "", "t.villemonteix@gmail.com"], ["Vittaut", "Jean-No\\u00ebl", "", "jean-noel.vittaut@univ-paris8.fr"], ["Wertz", "Harald", "", "hw@ai.univ-paris8.fr"], ["YOUEGO", "CHRISTINE", "", "moyoue@yahoo.fr"], ["berthier", "patrick", "", "patrick.berthier@yahoo.fr"], ["chaumet", "pierre-olivier", "chaumet", "pochaumet@hotmail.fr"], ["danjaume", "g\\u00e9raldine", "racchini", "gracchini@free.fr"], ["feat", "jym", "", "jym.feat@iedparis8.net"], ["galand", "charles", "", "charles.galand@hotmail.fr"], ["leclere", "maryvonne", "", "maryvonne.leclere@iedparis8.net"], ["marion", "catherine", "Lissajoux", "catherine.marion@iedparis8.net"], ["molinie", "magali", "", "magali.molinie@iedparis8.net"], ["mounard", "michel", "", "michelmounard@hotmail.com"], ["raphaele", "miljkovitch", "", "raphaele.miljkovitch@iedparis8.net"], ["silke", "schauder", "", "silke.schauder@iedparis8.net"], ["vaillant", "Laurence", "", "laurence.vaillant02@univ-paris8.fr"]]"""

from django.core.management.base import BaseCommand
from optparse import make_option
from django.db import connections

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--annee',
                    action='store',
                    type="int",
                    dest='annee',
                    default=None,
                    help='annee de remontee'),
    )

    def handle(self, *args, **options):
        result =  json.loads(j)
        for x in result:
            Titulaire.objects.get_or_create(
                nom_pat =x[0],
                nom_usuel =x[2],
                prenom =x[1],
                mail = x[3]
            )