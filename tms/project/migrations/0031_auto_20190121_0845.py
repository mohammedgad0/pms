# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-21 08:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_auto_20190121_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltask',
            name='parent',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project.HistoricalTask'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='parent',
        ),
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_task', to='project.Task'),
        ),
    ]
