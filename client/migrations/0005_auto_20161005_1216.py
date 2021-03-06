# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 10:16
from __future__ import unicode_literals

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20161005_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='allegati_autocertificazione',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='altri_allegati',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='attestati',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='attrribuzione_pi',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='bilancio_anno_corso',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='bilancio_ultimi_2',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='certificato_camerale',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='cf_doc',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='contratto',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='doc',
            field=models.FileField(blank=True, upload_to=client.models.for_id),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='mod_unico_anno_prec',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='mod_unico_anno_prec_2',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='preventivi',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
