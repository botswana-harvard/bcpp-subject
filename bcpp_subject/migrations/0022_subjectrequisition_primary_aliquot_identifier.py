# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0021_auto_20170217_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectrequisition',
            name='primary_aliquot_identifier',
            field=models.CharField(editable=False, max_length=18, null=True, unique=True),
        ),
    ]
