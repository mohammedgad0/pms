# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-21 08:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_auto_20190120_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='parent',
            field=models.ManyToManyField(blank=True, related_name='parent_task', to='project.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_phase', to='project.ProjectPhase'),
        ),
    ]
