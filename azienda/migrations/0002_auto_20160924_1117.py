# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cap',
            field=models.CharField(max_length=20, verbose_name='C.a.p.'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.CharField(max_length=150, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='company',
            name='numeroCivico',
            field=models.CharField(max_length=10, verbose_name='Numero Civico'),
        ),
    ]
