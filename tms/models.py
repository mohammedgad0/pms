# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Project(models.Model):
    name = models.CharField(db_column='Name', max_length=250, blank=True, null=True)  # Field name made lowercase.
    start = models.DateField(db_column='Start', blank=True, null=True)  # Field name made lowercase.
    end = models.DateField(blank=True, null=True)
    teamname = models.CharField(db_column='TeamName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId', blank=True, null=True)  # Field name made lowercase.
    statusid = models.IntegerField(db_column='StatusId', blank=True, null=True)  # Field name made lowercase.
    openedby = models.CharField(db_column='OpenedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='OpenedDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.CharField(db_column='ClosedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    canceledby = models.CharField(db_column='CanceledBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    canceleddate = models.DateTimeField(db_column='CanceledDate', blank=True, null=True)  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project'
