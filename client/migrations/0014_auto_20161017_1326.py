# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-17 11:26
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_auto_20161007_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='allegati_autocertificazione',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='altri_allegati',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='attestati',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='attrribuzione_pi',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='bilancio_anno_corso',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='bilancio_ultimi_2',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='certificato_camerale',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='cf_doc',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='contratto',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='doc',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='mod_unico_anno_prec',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='mod_unico_anno_prec_2',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='preventivi',
            field=models.FileField(blank=True, storage=client.models.CreateFolderUser(location='/media/'), upload_to=''),
        ),
    ]
