# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-08 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20190108_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('saved', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Employee')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Department')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('status', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_phases', to='project.Employee')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.ProjectPhase')),
                ('phase', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='project.Phase')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_phases', to='project.Employee')),
            ],
        ),
        migrations.AddField(
            model_name='phase',
            name='projects',
            field=models.ManyToManyField(related_name='phases', through='project.ProjectPhase', to='project.Project'),
        ),
    ]