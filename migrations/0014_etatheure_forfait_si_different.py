# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0013_allecannuel_validation_recrutement_directeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='etatheure',
            name='forfait_si_different',
            field=models.FloatField(default=1, null=True, blank=True),
        ),
    ]
