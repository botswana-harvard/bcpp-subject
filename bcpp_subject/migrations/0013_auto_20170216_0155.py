# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-15 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0012_auto_20170215_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousconsent',
            name='slug',
            field=models.CharField(db_index=True, editable=False, help_text='a field used for quick search', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='historicalanonymousconsent',
            name='slug',
            field=models.CharField(db_index=True, editable=False, help_text='a field used for quick search', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='historicalhivlinkagetocare',
            name='initiated',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True, verbose_name='[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] Did you [start/restart] ART since we spoke with you on last_visit_date?'),
        ),
        migrations.AlterField(
            model_name='historicalhivlinkagetocare',
            name='initiated_clinic_community',
            field=models.CharField(help_text='Indicate the community name', max_length=50, null=True, verbose_name='In which community is this clinic located'),
        ),
        migrations.AlterField(
            model_name='historicalhivlinkagetocare',
            name='initiated_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='When did you start/restart ART?'),
        ),
        migrations.AlterField(
            model_name='hivlinkagetocare',
            name='initiated',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True, verbose_name='[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] Did you [start/restart] ART since we spoke with you on last_visit_date?'),
        ),
        migrations.AlterField(
            model_name='hivlinkagetocare',
            name='initiated_clinic_community',
            field=models.CharField(help_text='Indicate the community name', max_length=50, null=True, verbose_name='In which community is this clinic located'),
        ),
        migrations.AlterField(
            model_name='hivlinkagetocare',
            name='initiated_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='When did you start/restart ART?'),
        ),
    ]