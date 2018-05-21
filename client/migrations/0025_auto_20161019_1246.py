# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-19 10:46
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0024_auto_20161019_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='attrribuzione_pi',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location=client.models.for_id), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='certificato_camerale',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location=client.models.for_id), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='cf_doc',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location=client.models.for_id), upload_to=''),
        ),
    ]
