# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-22 15:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20160924_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('Can_View', 'Può Visualizzare la Lista'),)},
        ),
    ]
