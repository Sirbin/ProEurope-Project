# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-10 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0032_auto_20161028_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='cf',
            field=models.CharField(max_length=16, verbose_name='Codice Fiscale'),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='donna_uomo',
            field=models.CharField(default=0, max_length=50, null=True, verbose_name='Uomo'),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='donna_uomo_1',
            field=models.CharField(default=0, max_length=50, null=True, verbose_name='Donna'),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='meno_di_35',
            field=models.CharField(default=0, max_length=15, null=True, verbose_name='Meno di 35'),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='numero_dipendenti',
            field=models.CharField(default=0, max_length=15, null=True, verbose_name='Numero Dipendenti'),
        ),
    ]
