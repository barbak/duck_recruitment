# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='titulaire',
            options={'ordering': ['nom_pat']},
        ),
        migrations.AlterField(
            model_name='agent',
            name='common_name',
            field=models.CharField(max_length=100, null=True, verbose_name="Nom d'\xe9poux", blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='first_name1',
            field=models.CharField(max_length=100, null=True, verbose_name='Pr\xe9nom'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='last_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Nom patronymique'),
        ),
    ]
