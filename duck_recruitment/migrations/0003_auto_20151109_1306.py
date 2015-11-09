# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0002_auto_20151106_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ratrapage', models.FloatField(null=True, verbose_name='rattrapage', blank=True)),
                ('proratisation', models.FloatField(null=True, verbose_name='proratisation', blank=True)),
                ('value_1', models.FloatField(null=True, verbose_name='premier', blank=True)),
                ('value_2', models.FloatField(null=True, verbose_name='deuxi\xe8me', blank=True)),
                ('_forfait_value', models.FloatField(null=True, blank=True)),
                ('_hf_value', models.FloatField(null=True, blank=True)),
                ('etat_heure', models.ForeignKey(to='duck_recruitment.EtatHeure')),
            ],
        ),
        migrations.CreateModel(
            name='Forfait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('annee', models.IntegerField(default=2015)),
                ('etape', models.ForeignKey(to='duck_recruitment.EtapeVet')),
            ],
        ),
        migrations.CreateModel(
            name='HeureForfait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('annee', models.IntegerField(default=2015)),
                ('semestriel', models.BooleanField(default=False)),
                ('proratise', models.BooleanField(default=True, verbose_name='Fixe')),
                ('etape', models.ForeignKey(to='duck_recruitment.EtapeVet')),
            ],
        ),
        migrations.CreateModel(
            name='HorsForfait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('annee', models.IntegerField(default=2015)),
                ('etape', models.ForeignKey(to='duck_recruitment.EtapeVet')),
            ],
        ),
        migrations.CreateModel(
            name='StatutEtatHeure',
            fields=[
                ('code', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='TypeActe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=60)),
                ('type_forfait', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeEc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=60)),
                ('etape', models.ForeignKey(to='duck_recruitment.EtapeVet')),
            ],
        ),
        migrations.CreateModel(
            name='TypeEtatHeure',
            fields=[
                ('code', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=30, verbose_name='Label')),
            ],
        ),
        migrations.AddField(
            model_name='horsforfait',
            name='type_acte',
            field=models.ForeignKey(to='duck_recruitment.TypeActe'),
        ),
        migrations.AddField(
            model_name='heureforfait',
            name='type_ec',
            field=models.ForeignKey(to='duck_recruitment.TypeEc'),
        ),
        migrations.AddField(
            model_name='forfait',
            name='type_acte',
            field=models.ForeignKey(to='duck_recruitment.TypeActe'),
        ),
        migrations.AddField(
            model_name='forfait',
            name='type_ec',
            field=models.ForeignKey(to='duck_recruitment.TypeEc'),
        ),
        migrations.AddField(
            model_name='acte',
            name='type_acte',
            field=models.ForeignKey(to='duck_recruitment.TypeActe'),
        ),
    ]
