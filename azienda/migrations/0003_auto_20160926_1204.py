# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-26 10:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('azienda', '0002_auto_20160924_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='Cellulare',
            new_name='cellulare',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='Fax',
            new_name='fax',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='TelefonoFisso',
            new_name='telefonoFisso',
        ),
    ]
