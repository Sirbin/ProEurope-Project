# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 17:02
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20161006_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='doc',
            field=models.FileField(blank=True, upload_to='', verbose_name=client.models.CreateFolderUser()),
        ),
    ]