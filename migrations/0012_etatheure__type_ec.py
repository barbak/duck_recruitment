# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0011_etatheure_coeff'),
    ]

    operations = [
        migrations.AddField(
            model_name='etatheure',
            name='_type_ec',
            field=models.CharField(max_length=1, null=True, verbose_name="cache pour le type de l'ec"),
        ),
    ]
