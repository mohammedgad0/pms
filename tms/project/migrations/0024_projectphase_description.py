# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-01-09 09:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20190109_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphase',
            name='description',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
    ]