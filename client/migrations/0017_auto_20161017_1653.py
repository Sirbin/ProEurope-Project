# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 14:53
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0016_documentfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentfile',
            old_name='doc',
            new_name='docFile',
        ),
        migrations.AddField(
            model_name='clientusercompany',
            name='doc',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
    ]
