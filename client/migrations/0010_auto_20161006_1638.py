# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_clientusercompany_data_mod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusercompany',
            name='attrribuzione_pi',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='cf_doc',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='clientusercompany',
            name='doc',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
