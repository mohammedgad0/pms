from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=250)  # Field name made lowercase.
    start = models.DateField(db_column='Start')  # Field name made lowercase.
    end = models.DateField()
    teamname = models.CharField(db_column='TeamName', max_length=100)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=250)  # Field name made lowercase.
    creationby = models.CharField(db_column='CreationBy', max_length=20)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId')  # Field name made lowercase.
    statusid = models.IntegerField(db_column='StatusId')  # Field name made lowercase.
    openby = models.CharField(db_column='OpenBy', max_length=20)  # Field name made lowercase.
    opendate = models.DateTimeField(db_column='OpenDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.CharField(db_column='ClosedBy', max_length=20)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    cancelby = models.CharField(db_column='CancelBy', max_length=20)  # Field name made lowercase.
    canceldate = models.DateTimeField(db_column='CancelDate', blank=True, null=True)  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project'


class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    projectid = models.IntegerField(db_column='ProjectId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=2500)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate')  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    assigndate = models.DateTimeField(db_column='AssignDate')  # Field name made lowercase.
    realstartdate = models.DateTimeField(db_column='RealStartDate')  # Field name made lowercase.
    finishby = models.IntegerField(db_column='FinishBy')  # Field name made lowercase.
    finishdate = models.DateTimeField(db_column='FinishDate')  # Field name made lowercase.
    cancelby = models.IntegerField(db_column='CancelBy')  # Field name made lowercase.
    canceldate = models.DateTimeField(db_column='CancelDate')  # Field name made lowercase.
    closeby = models.IntegerField(db_column='CloseBy')  # Field name made lowercase.
    closedate = models.DateTimeField(db_column='CloseDate')  # Field name made lowercase.
    closereson = models.CharField(db_column='CloseReson', max_length=500)  # Field name made lowercase.
    lastedit = models.DateTimeField(db_column='LastEdit')  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task'


class TaskStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.IntegerField(db_column='Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task_status'


class ProjectStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.IntegerField(db_column='Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project_status'


class Employee(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    empid = models.CharField(db_column='EmpId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='IsManager', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=45, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'

class Department(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='ManagerId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'

class Sheet(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    empid = models.BigIntegerField(db_column='EmpId', blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
    taskdesc = models.CharField(_('Task Descreption'),db_column='TaskDesc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    TASK_STATUS = (
        ('m', _('Master')),
        ('h', _('Help')),
    )
    tasktype = models.CharField(_('Task type'), max_length=1, choices=TASK_STATUS, db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(_('Duration'),db_column='Duration',blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    editedate = models.DateField(db_column='EditeDate', blank=True, null=True)  # Field name made lowercase.
    ifsubmitted = models.IntegerField(db_column='IfSubmitted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sheet'
