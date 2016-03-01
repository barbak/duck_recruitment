# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0007_auto_20160212_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='etatheure',
            name='_ratachement',
            field=models.FloatField(default=None, null=True, verbose_name='cache pour le ratachement'),
        ),
    ]
