# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0009_auto_20160213_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='etatheure',
            name='date_validation_annuel',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='etatheure',
            name='date_validation_premier_semestre',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='etatheure',
            name='date_validation_rattrapage',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='etatheure',
            name='is_valid_annuel',
            field=models.BooleanField(default=False, verbose_name="Valider l'\xe9tat recapitulatif"),
        ),
        migrations.AddField(
            model_name='etatheure',
            name='is_valid_premier_semestre',
            field=models.BooleanField(default=False, verbose_name="Valider l'\xe9tat du premier semestre"),
        ),
        migrations.AddField(
            model_name='etatheure',
            name='is_valid_rattrapage',
            field=models.BooleanField(default=False, verbose_name='Valider la proratisation'),
        ),
        migrations.AlterField(
            model_name='etatheure',
            name='valider',
            field=models.BooleanField(default=False, verbose_name='validation du prof'),
        ),
    ]
