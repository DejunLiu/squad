# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-18 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_project_build_completion_threshold'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testrun',
            unique_together=set([('build', 'job_id')]),
        ),
    ]