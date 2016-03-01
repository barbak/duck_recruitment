# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0010_auto_20160215_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='etatheure',
            name='coeff',
            field=models.FloatField(default=1, null=True, blank=True),
        ),
    ]
