# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-11 13:53
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0034_auto_20170211_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientusercompany',
            name='spese_altro',
            field=models.CharField(default='', max_length=150, verbose_name='Altre Spese'),
        ),
        migrations.AddField(
            model_name='clientusercompany',
            name='tipologia_altro',
            field=models.CharField(default='', max_length=150, verbose_name='Altro'),
        ),
        migrations.AddField(
            model_name='clientusercompany',
            name='visura_camerale',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(directory_permissions_mode=None, location=client.models.for_id), upload_to=client.models.for_id),
        ),
    ]
