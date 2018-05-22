# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-03 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientUserCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('denominazione', models.CharField(max_length=255, verbose_name='Denominazioe Ditta')),
                ('ditta', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=150, verbose_name='Nome')),
                ('cognome', models.CharField(max_length=150, verbose_name='Cognome')),
                ('indirizzo', models.CharField(max_length=250, verbose_name='Indirizzo')),
                ('citta', models.CharField(max_length=150, verbose_name='Città')),
                ('comune', models.CharField(max_length=100, verbose_name='Comune')),
                ('cap', models.CharField(max_length=20, verbose_name='C.a.p.')),
                ('piva', models.CharField(max_length=14, verbose_name='P.iva')),
                ('cf', models.CharField(max_length=15, verbose_name='Codice Fiscale')),
                ('telefonoFisso1', models.CharField(max_length=15, null=True, verbose_name='Telfono')),
                ('telefonoFisso2', models.CharField(max_length=15, null=True, verbose_name='Telfono Altro')),
                ('cellulare1', models.CharField(max_length=15, verbose_name='Celluare')),
                ('cellulare2', models.CharField(max_length=15, verbose_name='Celluare Altro')),
                ('url_sito', models.CharField(max_length=255)),
                ('fax', models.CharField(max_length=15, verbose_name='Fax')),
                ('email', models.CharField(max_length=150, verbose_name='E-mail')),
                ('pec', models.CharField(max_length=150, verbose_name='pec')),
                ('data_ins', models.DateTimeField(auto_now=True, verbose_name='Data inserimento')),
                ('note', models.CharField(max_length=255, verbose_name='Note')),
                ('tipologia', models.CharField(max_length=100, verbose_name='Tipologia')),
                ('numero_dipendenti', models.CharField(max_length=15, verbose_name='Numero Dipendenti')),
                ('meno_di_35', models.CharField(max_length=15, verbose_name='Meno di 35')),
                ('donna_uomo', models.CharField(max_length=50, verbose_name='Uomo')),
                ('donna_uomo_1', models.CharField(max_length=50, verbose_name='Donna')),
                ('spese', models.CharField(max_length=15, verbose_name='Spese')),
                ('note_1', models.CharField(max_length=500, verbose_name='Dettaglio Spese')),
                ('tipologia_richiesta', models.CharField(max_length=50, verbose_name='Tipologia Spese')),
                ('Procedure_1', models.CharField(max_length=155)),
                ('Procedure_2', models.CharField(max_length=155)),
                ('Procedure_3', models.CharField(max_length=155)),
            ],
        ),
    ]