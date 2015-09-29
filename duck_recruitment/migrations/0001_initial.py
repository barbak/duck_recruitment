# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CCOURS_Individu',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column=b'INDIV_ID')),
                ('numero', models.IntegerField(db_column=b'INDIV_NUMERO')),
                ('civilite', models.CharField(max_length=20, db_column=b'INDIV_CIVILITE')),
                ('nom_pat', models.CharField(max_length=2000, db_column=b'INDIV_NOM_PAT')),
                ('nom_usuel', models.CharField(max_length=2000, db_column=b'INDIV_NOM_USUEL')),
                ('prenom', models.CharField(max_length=2000, db_column=b'INDIV_PRENOM')),
                ('dnaissance', models.DateField(db_column=b'INDIV_DNAISSANCE')),
                ('dept_naissa', models.CharField(max_length=3, db_column=b'INDIV_DEPT_NAISSA')),
                ('ville_naiss', models.CharField(max_length=2000, db_column=b'INDIV_VILLE_NAISS')),
                ('pays_naiss', models.CharField(max_length=3, db_column=b'INDIV_PAYS_NAISS')),
                ('pays_nationalite', models.CharField(max_length=3, db_column=b'INDIV_PAYS_NATIONALITE')),
                ('sitfam', models.CharField(max_length=1, db_column=b'INDIV_SITFAM')),
                ('no_insee', models.CharField(max_length=13, db_column=b'INDIV_NO_INSEE')),
                ('cle_insee', models.IntegerField(db_column=b'INDIV_CLE_INSEE')),
                ('mail', models.CharField(max_length=2000, db_column=b'INDIV_MAIL')),
                ('login', models.CharField(max_length=2000, db_column=b'INDIV_LOGIN')),
                ('password', models.CharField(max_length=2000, db_column=b'INDIV_PASSWORD')),
                ('mangue_id', models.IntegerField(db_column=b'MANGUE_ID')),
                ('etat_id', models.IntegerField(db_column=b'ETAT_ID')),
            ],
            options={
                'db_table': 'INDIVIDU',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ccours_ref_id', models.IntegerField(null=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Nom patronymique')),
                ('common_name', models.CharField(max_length=30, null=True, verbose_name="Nom d'\xe9poux", blank=True)),
                ('first_name1', models.CharField(max_length=30, verbose_name='Pr\xe9nom')),
                ('first_name2', models.CharField(max_length=30, null=True, verbose_name='Deuxi\xe8me pr\xe9nom', blank=True)),
                ('first_name3', models.CharField(max_length=30, null=True, verbose_name='Troisi\xe8me pr\xe9nom', blank=True)),
                ('personal_email', models.EmailField(max_length=254, unique=True, null=True, verbose_name=b'Email')),
                ('sex', models.CharField(max_length=1, null=True, verbose_name='sexe', choices=[(b'M', b'Homme'), (b'F', b'Femme')])),
                ('birthday', models.DateField(null=True, verbose_name=b'date de naissance')),
            ],
        ),
        migrations.CreateModel(
            name='EC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=8)),
                ('label', models.CharField(max_length=128)),
                ('description', models.TextField()),
            ],
        ),
    ]
