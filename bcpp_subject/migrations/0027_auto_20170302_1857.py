# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-02 16:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcpp_subject', '0026_subjectrequisition_study_site_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='pimavl',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='historicalpimavl',
            name='quota_pk',
        ),
        migrations.RemoveField(
            model_name='historicalpimavl',
            name='request_code',
        ),
        migrations.RemoveField(
            model_name='pimavl',
            name='quota_pk',
        ),
        migrations.RemoveField(
            model_name='pimavl',
            name='request_code',
        ),
    ]