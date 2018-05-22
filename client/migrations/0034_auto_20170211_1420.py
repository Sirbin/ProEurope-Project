# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-11 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0033_auto_20161110_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientusercompany',
            name='codice_ateco',
            field=models.CharField(default='', max_length=25, verbose_name='Codice Ateco'),
        ),
        migrations.AddField(
            model_name='clientusercompany',
            name='numero_rea',
            field=models.CharField(default='', max_length=25, verbose_name='Numero Rea'),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='ditta',
            field=models.BooleanField(default=True, verbose_name='Società'),
        ),
    ]