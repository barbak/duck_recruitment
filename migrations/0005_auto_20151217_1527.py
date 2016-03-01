# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0004_remove_heureforfait_proratise'),
    ]

    operations = [
        migrations.AddField(
            model_name='ec',
            name='type',
            field=models.ForeignKey(blank=True, to='duck_recruitment.TypeEc', null=True),
        ),
        migrations.AddField(
            model_name='heureforfait',
            name='proratise',
            field=models.BooleanField(default=True, verbose_name='fixe '),
        ),
    ]
