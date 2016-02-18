# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0012_etatheure__type_ec'),
    ]

    operations = [
        migrations.AddField(
            model_name='allecannuel',
            name='validation_recrutement_directeur',
            field=models.BooleanField(default=False),
        ),
    ]
