# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import csv

from django_apogee.models import InsAdmEtp, Individu
from django.core.management.base import BaseCommand
from optparse import make_option
import requests
import simpleldap


ANNEE = 2015

class Command(BaseCommand):

    url = 'http://moodle.iedparis8.net/webservice/rest/server.php'
    token = '91361080b67ff676c3d7789e9e967ca2'

    ETAPES = [
        'L1NDRO',
        'L2NDRO',
        'L3NDRO',
        # droit
        'L1NPSY',
        'L2NPSY',
        'L3NPSY',
        # licence psy
        'L1NINF',
        'L2NINF',
        'L3NINF',
        # licence info
        'DSNPCA',
        # desu
        'M1NPCL',
        'M2NPCL',
        # clinique
        'M1NPEA',
        'M2NPEA',
        # enfance
        'M1NPST',
        'M2NPST',
        # social
        'L3NEDU',
        'M1NEFI',
        'M2NEFI'
        # education
    ]

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?')

    def get_ldap_student(self):
        filtre = '(&(uid=*)(mail=*etud*)(up8Diplome=*))'
        attr = [
            'sn',
            'givenName',
            'supannEtuId',
            'uid'
        ]
        search = {'base_dn': 'dc=univ-paris8,dc=fr', 'list': 'sn,givenName,supannEtuId'}
        conn = simpleldap.Connection('ldap.etud.univ-paris8.fr',
                                     dn='cn=admin,dc=univ-paris8,dc=fr',
                                     search_defaults=search,
                                     password='p8SARiH3')
        results = conn.search(filtre,
                              # attrs=attr
                              )
        self.ldap_user = {x['supannEtuId'][0]: x['uid'][0] for x in results}

    # def get_ldap
    def get_all_user(self, cod_etp):
        resultats = []
        codes_etu = self.ldap_user.keys()

        for individu in Individu.objects.using('oracle').filter(etapes__cod_etp=cod_etp, etapes__cod_anu=ANNEE,
                                                                etapes__eta_iae='E'):
            if str(individu.cod_etu) in codes_etu:
                cod_etu = str(individu.cod_etu)
                user = {
                    'username': self.ldap_user[cod_etu],
                    'firstname': individu.lib_pr1_ind,
                    'lastname': individu.lib_nom_pat_ind,
                    'cod_etu': cod_etu
                }
                resultats.append(user)
            else:
                self.errors.append([individu.cod_etu, individu.lib_nom_pat_ind, individu.lib_pr1_ind])

        return resultats

    def get_all_user_csv(self, users, cod_etp):
        result = [[user['username'], 'not cached', user['firstname'].title(),
                  user['lastname'].title(), '{}@foad.iedparis8.net'.format(user['cod_etu']),
                   'cas', user['cod_etu'], 'fr', cod_etp, 1] for user in users]
        return result

    def create_csv(self, users):
        with open('/vagrant/cohorts.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            champs = ['username', 'password', 'firstname', 'lastname',
                      'email', 'auth', 'idnumber', 'lang', 'cohort1', 'type1']
            spamwriter.writerow(champs)
            for row in users:
                spamwriter.writerow(row)

    def create_user_administratif(self, username):
        with open('/vagrant/cohorts_admistratif.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            champs = ['username', 'cohort1', 'type1']
            spamwriter.writerow(champs)
            for row in self.ETAPES:
                spamwriter.writerow([username, row, '3'])

    def handle(self, *args, **options):
        self.errors = []
        if options['username']:
            self.create_user_administratif(options['username'])
        else:
            self.get_ldap_student()
            all_user = []
            for cod_etp in self.ETAPES:
                users = self.get_all_user(cod_etp)
                all_user.extend(self.get_all_user_csv(users, cod_etp))
            self.create_csv(all_user)
            with open('/vagrant/erreurs.csv', 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in self.errors:
                    spamwriter.writerow(row)
