# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_recruitment', '0005_auto_20151217_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropEc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default='0', max_length=1, choices=[('0', 'Annuel'), ('1', 'Premier semestre'), ('2', 'Seconde semestre')])),
                ('annee', models.IntegerField(default=2015)),
                ('ec', models.ForeignKey(to='duck_recruitment.Ec')),
            ],
        ),
    ]
