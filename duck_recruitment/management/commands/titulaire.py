# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django_apogee.models import InsAdmEtp, Individu, Adresse, AnneeUni, ConfAnneeUni, EtpGererCge, InsAdmEtpInitial, \
    Etape
import csv
from duck_recruitment.models import Ec, EtapeVet, Titulaire
import json
__author__ = 'paul'
j= """[["BRIDOU", "Morgiane", "", "morgiane.bridou@iedparis8.net"], ["Arnaud", "Plagnol", "", "arnaud.plagnol@iedparis8.net"], ["Lionel", "Dagot", null, "lionel.dagot@iedparis8.net"], ["AMORIM", "Marilia", "DUFOUR", "mamorim@univ-paris8.fr"], ["Antoine", "Corinne", "", "corinne.antoine@iedparis8.net"], ["Baque", "Dominique", "", "dominique.baque@iedparis8.net"], ["Meunier", "Jean-Marc", "", "jean-marc.meunier@iedparis8.net"], ["Bardin", "Brigitte", "", "brigitte.bardin@univ-tlse2.fr"], ["Behra", "Timoth\\u00e9e", "", "timotheebehra.etu@gmail.com"], ["Bernard", "Gilles", "", "gilles.bernard@iedparis8.net"], ["COLIN", "Lucette", "", "lucettecolin@noos.fr"], ["CONTY", "LAurence", "Conty", "laurence.conty@gmail.com"], ["Chicharro", "Gladys", "", "gladyschicharro@hotmail.com"], ["DEBORDE", "Anne-Sophie", "", "anne-spohie.deborde@iedparis8.net"], ["DEMARCHI", "SAMUEL", "", "samuel.demarchi@univ-paris8.fr"], ["DUPUCH", "LAURENCE", "", "laurence.dupuch02@univ-paris8.fr"], ["DURIEZ", "NATHALIE", "TIQUET", "nathalie.duriez-tiquet@univ-paris8.fr"], ["DURIEZ", "NATHALIE", "TIQUET", "nathalie.duriez@iedparis8.net"], ["Dominique", "Baqu\\u00e9", null, "dombaque@orange.fr"], ["ELOY", "Florence", "", "florence_eloy@yahoo.fr"], ["Eriksen", "Anna", "Terzian", "anna.terzian@univ-paris8.fr"], ["Francoise", "Morange-Majoux", "Majoux", "francoise.morange-majoux@iedparis8.net"], ["GUENIF", "NACIRA", "SOUILAMAS", "nacira.guenif@univ-paris8.fr"], ["GUERAUD", "SABINE", "", "sabine.gueraud@univ-paris8.fr"], ["HENNION", "PATRICIA", "JACQUET", "patricia.hennion-jacquet@iedparis8.net"], ["HESS", "Remi", "", "remihess@noos.fr"], ["HOUILLON", "Jean-Charles", "", "jean-charles.houillon@iedparis8.net"], ["Habib", "Marianne", "", "marianne.habib@univ-paris8.fr"], ["Jean", "Laingui", null, "jean.laingui@iedparis8.net"], ["Juhan", "Michel", "", "michel.juhan@univ-paris8.fr"], ["LEFEVRE", "CAROLE", "", "carole.lefevre@iedparis8.net"], ["Laurent", "Jean-Paul", "", "jean-paul.laurent@iedparis8.net"], ["Lesourd", "Francis", "", "francis.lesourd@iedparis8.net"], ["Lujan", "Cristianh", "", "christian.lujan@iedparis8.net"], ["MARIAGE", "Jean-Jacques", "", "jjmariage@free.fr"], ["MASSE", "LAURENCE", "", "laurence.masse@iedparis8.net"], ["Gautier", "Agn\\u00e8s", "Gautier-Audebert", "agnes.gautier.audebert@neuf.fr"], ["MOREAU", "Didier", "", "didier.moreauparis8@gmail.com"], ["Marquez-D.", "Eduardo", "", "eduardo.marquez@iedparis8.net"], ["Mehat", "Jean", "", "jmehat@gmail.com"], ["Monica", "Macedo", "", "monica.macedo@iedparis8.net"], ["Morisse", "Martine", "", "martine.morisse@iedparis8.net"], ["Morisse", "Martine", "", "martine.morisse@univ-paris8.fr"], ["NIVARD", "Jacqueline", "BIGOURDAN", "jacqueline.nivard@iedparis8.net"], ["PAPPA", "ANNA", "", "ap@ai.univ-paris8.fr"], ["Perrotin", "Marie-Liesse", "", "marie-liesse.perrotin@iedparis8.net"], ["STILGENBAUER", "Jean-Louis", "", "jean-louis.stilgenbauer@iedparis8.net"], ["Villemonteix", "Thomas", "", "t.villemonteix@gmail.com"], ["Vittaut", "Jean-No\\u00ebl", "", "jean-noel.vittaut@univ-paris8.fr"], ["Wertz", "Harald", "", "hw@ai.univ-paris8.fr"], ["YOUEGO", "CHRISTINE", "", "moyoue@yahoo.fr"], ["berthier", "patrick", "", "patrick.berthier@yahoo.fr"], ["chaumet", "pierre-olivier", "chaumet", "pochaumet@hotmail.fr"], ["danjaume", "g\\u00e9raldine", "racchini", "gracchini@free.fr"], ["feat", "jym", "", "jym.feat@iedparis8.net"], ["galand", "charles", "", "charles.galand@hotmail.fr"], ["leclere", "maryvonne", "", "maryvonne.leclere@iedparis8.net"], ["marion", "catherine", "Lissajoux", "catherine.marion@iedparis8.net"], ["molinie", "magali", "", "magali.molinie@iedparis8.net"], ["mounard", "michel", "", "michelmounard@hotmail.com"], ["raphaele", "miljkovitch", "", "raphaele.miljkovitch@iedparis8.net"], ["silke", "schauder", "", "silke.schauder@iedparis8.net"], ["vaillant", "Laurence", "", "laurence.vaillant02@univ-paris8.fr"]]"""

from django.core.management.base import BaseCommand
from optparse import make_option
from django.db import connections
import requests
import simpleldap
class Command(BaseCommand):


    option_list = BaseCommand.option_list + (
        make_option('--annee',
                    action='store',
                    type="int",
                    dest='annee',
                    default=None,
                    help='annee de remontee'),
    )
    'npeteinatos;not cached;nikos;peitenatos;nikos.peteinatos@iedparis8.net;cas;14511794;fr;L1NPSY;1'
    def handle(self, *args, **options):
        url = 'http://moodle.iedparis8.net/webservice/rest/server.php'
        wsfunction = 'core_user_create_users'
        param = {
            'wstoken': '91361080b67ff676c3d7789e9e967ca2',
            'wsfunction': wsfunction,
            'moodlewsrestformat': 'json',
            'users[0][username]': 'npeteinatos',
            'users[0][password]': 'not cached',
            'users[0][firstname]': 'nikos',
            'users[0][lastname]': 'peitenatos',
            'users[0][email]': 'nikos.peteinatos@iedparis8.net',
            'users[0][auth]': 'cas',
            'users[0][idnumber]': '14511794',
            'users[0][lang]': 'fr',
            # '': '',

        }
        p = {
            'wstoken': '91361080b67ff676c3d7789e9e967ca2',
            'wsfunction': 'core_user_get_users_by_field',
            'moodlewsrestformat': 'json',
            'field': 'username',
            'values[0]': 'npeteinatos'
        }
        result = requests.post(url, data=p).json()[0]

        param['wsfunction'] = 'core_user_update_users'
        print result['id']
        param['users[0][id]'] = result['id']
        param.pop('users[0][password]')

        print param
        result = requests.post(url, data=param).json()

        print result
        param = {
                'wstoken': '91361080b67ff676c3d7789e9e967ca2',
                'wsfunction': 'core_cohort_add_cohort_members',
                'moodlewsrestformat': 'json',
                'members[0][cohorttype][type]': 'idnumber',
                'members[0][cohorttype][value]':  'L3NEDU',
                'members[0][usertype][type]': 'username',
                'members[0][usertype][value]': 'npeteinatos',
            }
        result = requests.post(url, data=param).json()
        print result

        param = {
                'wstoken': '91361080b67ff676c3d7789e9e967ca2',
                'wsfunction': 'core_cohort_add_cohort_members',
                'moodlewsrestformat': 'json',
                'members[0][cohorttype][type]': 'idnumber',
                'members[0][cohorttype][value]':  'L3NEDU',
                'members[0][usertype][type]': 'username',
                'members[0][usertype][value]': 'npeteinatos',
            }
        result = requests.post(url, data=param).json()
        print result
        # if False:
        #     filtre = '(&(uid=*)(mail=*etud*)(up8Diplome=L3NEDU))'
        #     attr = [
        #         'sn',
        #         'givenName',
        #         'supannEtuId',
        #         'uid'
        #     ]
        #     search = {'base_dn': 'dc=univ-paris8,dc=fr', 'list': 'sn,givenName,supannEtuId'}
        #     conn = simpleldap.Connection('ldap.etud.univ-paris8.fr',
        #                                  dn='cn=admin,dc=univ-paris8,dc=fr',
        #                                  search_defaults=search,
        #                                  password='p8SARiH3')
        #     results = conn.search(filtre,
        #                           # attrs=attr
        #                           )
        #     # print len(results)
        #     r = {}
        #     with open('eggs.csv', 'wb') as csvfile:
        #         spamwriter = csv.writer(csvfile, delimiter=' ',
        #                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #
        #         for x in results:
        #             spamwriter.writerow([x['supannEtuId'][0], x['uid'][0]])
        # else:
        #     result = {}
        #     with open('eggs.csv', 'rb') as csvfile:
        #         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        #         for row in spamreader:
        #             result[row[0]] = row[1]
        #     r = []
        #     for x in InsAdmEtpInitial.inscrits.using('oracle').filter(cod_etp='L3NEDU'):
        #         if str(x.cod_ind.cod_etu) in result.keys():
        #             cod_etu = str(x.cod_ind.cod_etu)
        #             a = [result[cod_etu], 'not cached', x.cod_ind.lib_pr1_ind, x.cod_ind.lib_nom_pat_ind,
        #                  '{}@foad.iedparis8.net'.format(cod_etu), 'cas', cod_etu, 'fr', 'L3NEDU', 1]
        #             r.append(a)
        #     with open('cohorts.csv', 'wb') as csvfile:
        #         spamwriter = csv.writer(csvfile, delimiter=';',
        #                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #         champs = ['username', 'password', 'firstname', 'lastname',
        #                   'email', 'auth', 'idnumber', 'lang', 'cohort1', 'type1']
        #         spamwriter.writerow(champs)
        #         for row in r:
        #             spamwriter.writerow(row)
