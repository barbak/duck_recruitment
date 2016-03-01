# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0006_propec'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdresseCcours',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column='ADR_ID')),
                ('cp', models.CharField(max_length=5, null=True, db_column='ADR_CP', blank=True)),
                ('insee', models.CharField(max_length=5, null=True, db_column='ADR_INSEE', blank=True)),
                ('adresse', models.CharField(max_length=2000, null=True, db_column='ADR_ADRESSE', blank=True)),
                ('adresse_suite', models.CharField(max_length=2000, null=True, db_column='ADR_ADRESSE_SUITE')),
                ('commune', models.CharField(max_length=2000, null=True, db_column='ADR_COMMUNE')),
                ('pays', models.CharField(max_length=3, null=True, db_column='ADR_PAYS')),
                ('port', models.CharField(max_length=2000, null=True, verbose_name='telephone portable', db_column='ADR_PORT')),
                ('tel', models.CharField(max_length=2000, null=True, verbose_name='telephone fixe', db_column='ADR_TEL')),
                ('voie', models.CharField(max_length=50, null=True, db_column='ADR_VOIE')),
            ],
            options={
                'db_table': 'ADRESSE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TypeAdresse',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True, db_column='TYPA_ID')),
                ('libelle', models.CharField(max_length=2000, null=True, db_column='TYPA_ADRESSE')),
            ],
            options={
                'db_table': 'TYPE_ADRESSE',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='etatheure',
            name='_forfait',
            field=models.FloatField(default=None, null=True, verbose_name='cache pour le forfait'),
        ),
    ]
