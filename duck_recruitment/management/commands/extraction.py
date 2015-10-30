# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import csv

from django_apogee.models import InsAdmEtp, Individu
from django.core.management.base import BaseCommand
from optparse import make_option
import requests
import simpleldap

from duck_recruitment.models import Agent

ANNEE = 2015

class Command(BaseCommand):


    def handle(self, *args, **options):
        with open('/vagrant/extraction.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for agent in Agent.objects.filter(allecannuel__etatheure__isnull=False):
                spamwriter.writerow([agent.last_name, agent.first_name])
                for allec in agent.allecannuel_set.all():
                    spamwriter.writerow(allec.all_ec_lib())


