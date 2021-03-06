# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-08 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20190108_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phase',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='phase',
            name='department',
        ),
        migrations.RemoveField(
            model_name='phase',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='phase',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectphase',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Phase',
        ),
        migrations.DeleteModel(
            name='ProjectPhase',
        ),
    ]
