# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-23 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azienda', '0009_auto_20161024_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cf',
            field=models.CharField(max_length=16, verbose_name='Codice Fiscale'),
        ),
    ]
