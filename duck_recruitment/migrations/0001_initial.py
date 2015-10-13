# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_apogee', '0003_auto_20151009_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='CCOURS_Individu',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column='INDIV_ID')),
                ('numero', models.IntegerField(db_column='INDIV_NUMERO')),
                ('civilite', models.CharField(max_length=20, db_column='INDIV_CIVILITE')),
                ('nom_pat', models.CharField(max_length=2000, db_column='INDIV_NOM_PAT')),
                ('nom_usuel', models.CharField(max_length=2000, db_column='INDIV_NOM_USUEL')),
                ('prenom', models.CharField(max_length=2000, db_column='INDIV_PRENOM')),
                ('dnaissance', models.DateField(db_column='INDIV_DNAISSANCE')),
                ('dept_naissa', models.CharField(max_length=3, db_column='INDIV_DEPT_NAISSA')),
                ('ville_naiss', models.CharField(max_length=2000, db_column='INDIV_VILLE_NAISS')),
                ('pays_naiss', models.CharField(max_length=3, db_column='INDIV_PAYS_NAISS')),
                ('pays_nationalite', models.CharField(max_length=3, db_column='INDIV_PAYS_NATIONALITE')),
                ('sitfam', models.CharField(max_length=1, db_column='INDIV_SITFAM')),
                ('no_insee', models.CharField(max_length=13, db_column='INDIV_NO_INSEE')),
                ('cle_insee', models.IntegerField(db_column='INDIV_CLE_INSEE')),
                ('mail', models.CharField(max_length=2000, db_column='INDIV_MAIL')),
                ('login', models.CharField(max_length=2000, db_column='INDIV_LOGIN')),
                ('password', models.CharField(max_length=2000, db_column='INDIV_PASSWORD')),
                ('mangue_id', models.IntegerField(db_column='MANGUE_ID')),
                ('etat_id', models.IntegerField(db_column='ETAT_ID')),
            ],
            options={
                'db_table': 'INDIVIDU',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SettingsEtapes',
            fields=[
                ('etape_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_apogee.Etape')),
            ],
            options={
                'db_table': 'duck_inscription_settingsetape',
                'managed': False,
            },
            bases=('django_apogee.etape',),
        ),
        migrations.CreateModel(
            name='SettingsEtapeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'duck_inscription_settingsuser_etapes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SettingsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'duck_inscription_settingsuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('individu_id', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=10, null=True, choices=[('charge', 'Charg\xe9 de cours'), ('tit', 'Titulaire')])),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='Nom patronymique')),
                ('common_name', models.CharField(max_length=30, null=True, verbose_name="Nom d'\xe9poux", blank=True)),
                ('first_name1', models.CharField(max_length=30, null=True, verbose_name='Pr\xe9nom')),
                ('personal_email', models.EmailField(max_length=254, unique=True, null=True, verbose_name='Email')),
                ('birthday', models.DateField(null=True, verbose_name='date de naissance')),
            ],
        ),
        migrations.CreateModel(
            name='AllEcAnnuel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annee', models.CharField(default='2015', max_length=4)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('agent', models.ForeignKey(to='duck_recruitment.Agent')),
            ],
        ),
        migrations.CreateModel(
            name='Ec',
            fields=[
                ('id', models.CharField(max_length=8, serialize=False, verbose_name='id element', primary_key=True)),
                ('code_ec', models.CharField(unique=True, max_length=8, verbose_name='code element')),
                ('type_ec', models.CharField(max_length=4, verbose_name='type element')),
                ('lib_ec', models.CharField(max_length=120, verbose_name='libelle')),
                ('tem_sec', models.CharField(max_length=1, verbose_name='tem_sec')),
            ],
        ),
        migrations.CreateModel(
            name='EtapeVet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cod_vrs_vet', models.CharField(max_length=3)),
                ('cod_cmp', models.CharField(max_length=3)),
                ('cod_etp', models.ForeignKey(to='django_apogee.Etape')),
            ],
        ),
        migrations.CreateModel(
            name='EtatHeure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forfaitaire', models.BooleanField(default=True)),
                ('nombre_heure_estime', models.FloatField(null=True, blank=True)),
                ('valider', models.BooleanField(default=False)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('all_ec_annuel', models.ForeignKey(to='duck_recruitment.AllEcAnnuel')),
                ('ec', models.ForeignKey(to='duck_recruitment.Ec')),
            ],
        ),
        migrations.CreateModel(
            name='InvitationEc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annee', models.CharField(default='2015', max_length=4)),
                ('email', models.EmailField(max_length=254)),
                ('valider', models.BooleanField(default=False)),
                ('numero', models.IntegerField(null=True)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('date_acceptation', models.DateField(null=True)),
                ('forfaitaire', models.BooleanField(default=True)),
                ('nombre_heure_estime', models.FloatField(null=True, blank=True)),
                ('ec', models.ForeignKey(to='duck_recruitment.Ec')),
            ],
        ),
        migrations.CreateModel(
            name='Titulaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(null=True, blank=True)),
                ('nom_pat', models.CharField(max_length=100, null=True)),
                ('nom_usuel', models.CharField(max_length=100, null=True, blank=True)),
                ('prenom', models.CharField(max_length=100, null=True)),
                ('dnaissance', models.DateField(null=True, blank=True)),
                ('mail', models.CharField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='ec',
            name='etape',
            field=models.ManyToManyField(to='duck_recruitment.EtapeVet'),
        ),
    ]
