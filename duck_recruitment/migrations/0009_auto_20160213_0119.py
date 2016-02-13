# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0008_etatheure__ratachement'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etatheure',
            old_name='_ratachement',
            new_name='_rattachement',
        ),
        migrations.AddField(
            model_name='etatheure',
            name='heure_statutaire',
            field=models.FloatField(default=0),
        ),
    ]
