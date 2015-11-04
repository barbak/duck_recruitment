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
    option_list = BaseCommand.option_list + (
        make_option('--annee',
                    action='store',
                    type="int",
                    dest='annee',
                    default=None,
                    help='annee de remontee'),
    )
    ETAPES = [
        'L1NPSY',
        'L2NPSY',
        'L3NPSY',
        'L1NINF',
        'L2NINF',
        'L3NINF',
        'DSNATA',
        'M1NPCL',
        'M2NPCL',
        'M1NPEA',
        'M2NPEA',
        'M1NPST',
        'M2NPST',
        'M1NEFI'
    ]

    def get_ldap_student(self, cod_etp):
        filtre = '(&(uid=*)(mail=*etud*)(up8Diplome={}))'.format(cod_etp)
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
        results = {x['supannEtuId'][0]: x['uid'][0] for x in results}
        return results

    def get_all_user(self, cod_etp):
        resultats = []
        ldap_user = self.get_ldap_student(cod_etp)
        codes_etu = ldap_user.keys()
        for individu in Individu.objects.using('oracle').filter(etapes__cod_etp=cod_etp, etapes__cod_anu=ANNEE,
                                                                etapes__eta_iae='E', etapes__tem_iae_prm='O'):
            if str(individu.cod_etu) in codes_etu:
                cod_etu = str(individu.cod_etu)
                user = {
                    'username': ldap_user[cod_etu],
                    'firstname': individu.lib_pr1_ind,
                    'lastname': individu.lib_nom_pat_ind,
                    'cod_etu': cod_etu
                }
                resultats.append(user)
        return resultats

    def get_all_user_csv(self, users, cod_etp):
        result = [[user['username'], 'not cached', user['firstname'],
                  user['lastname'], '{}@foad.iedparis8.net'.format(user['cod_etu']),
                   'cas', user['cod_etu'], 'fr', cod_etp, 1] for user in users]
        return result

    def create_user(self, user):
        param = {
            'wstoken': self.token,
            'wsfunction': 'core_user_create_users',
            'moodlewsrestformat': 'json',
            'users[0][username]': user['username'],
            'users[0][password]': 'not cached',
            'users[0][firstname]': user['firstname'],
            'users[0][lastname]': user['lastname'],
            'users[0][email]': '{}@foad.iedparis8.net'.format(user['cod_etu']),
            'users[0][auth]': 'cas',
            'users[0][idnumber]': user['cod_etu'],
            'users[0][lang]': 'fr',
        }
        result = requests.post(self.url, data=param).json()
        return result

    def create_users(self, users):
        param = {
            'wstoken': self.token,
            'wsfunction': 'core_user_create_users',
            'moodlewsrestformat': 'json'
        }
        for i, user in enumerate(users[:10]):
            param['users[{}][username]'.format(i)] = user['username']
            param['users[{}][password]'.format(i)] = 'not cached'
            param['users[{}][firstname]'.format(i)] = user['firstname']
            param['users[{}][lastname]'.format(i)] = user['lastname']
            param['users[{}][email]'.format(i)] = '{}@foad.iedparis8.net'.format(user['cod_etu'])
            param['users[{}][auth]'.format(i)] = 'cas'
            param['users[{}][idnumber]'.format(i)] = user['cod_etu']
            param['users[{}][lang]'.format(i)] = 'fr'
        result = requests.post(self.url, data=param).text
        return result

    def get_user(self, user):
        param = {
            'wstoken': self.token,
            'wsfunction': 'core_user_get_users_by_field',
            'moodlewsrestformat': 'json',
            'field': 'username',
            'values[0]': user['username']
        }
        result = requests.post(self.url, data=param).json()[0]
        return result

    def update_user(self, user):
        param = {
            'wstoken': self.token,
            'wsfunction': 'core_user_update_users',
            'moodlewsrestformat': 'json',
            'users[0][id]': user['id'],
            'users[0][username]': user['username'],
            'users[0][firstname]': user['firstname'],
            'users[0][lastname]': user['lastname'],
            'users[0][email]': '{}@foad.iedparis8.net'.format(user['cod_etu']),
            'users[0][auth]': 'cas',
            'users[0][idnumber]': user['cod_etu'],
            'users[0][lang]': 'fr',
        }
        result = requests.post(self.url, data=param).json()
        return result

    def add_cohorts(self, user, cod_etp):
        param = {
                'wstoken': self.token,
                'wsfunction': 'core_cohort_add_cohort_members',
                'moodlewsrestformat': 'json',
                'members[0][cohorttype][type]': 'idnumber',
                'members[0][cohorttype][value]':  cod_etp,
                'members[0][usertype][type]': 'username',
                'members[0][usertype][value]': user['username'],
            }
        result = requests.post(self.url, data=param).json()
        return result

    def remontee_user(self, user, cod_etp):
        print self.create_user(user)
        r = self.get_user(user)
        user['id'] = r['id']
        print self.update_user(user)
        # print self.add_cohorts(user, cod_etp)

    def create_csv(self, users, cod_etp):
        with open('/vagrant/cohorts_{}.csv'.format(cod_etp), 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            champs = ['username', 'password', 'firstname', 'lastname',
                      'email', 'auth', 'idnumber', 'lang', 'cohort1', 'type1']
            spamwriter.writerow(champs)
            for row in users:
                spamwriter.writerow(row)

    def handle(self, *args, **options):
        cod_etp = 'M1NEFI'
        all_user = []
        for cod_etp in self.ETAPES:
            users = self.get_all_user(cod_etp)
            all_user.extend(self.get_all_user_csv(users, cod_etp))
        self.create_csv(all_user, '')



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

