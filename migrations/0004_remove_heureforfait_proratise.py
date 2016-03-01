# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0003_auto_20151109_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heureforfait',
            name='proratise',
        ),
    ]
