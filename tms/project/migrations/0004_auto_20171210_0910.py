# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-10 06:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_employee1_sheet1'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApfDeptView',
            fields=[
                ('id', models.IntegerField(db_column='Id', primary_key=True, serialize=False)),
                ('dept_code', models.CharField(blank=True, db_column='DEPT_CODE', max_length=5, null=True)),
                ('dept_name', models.CharField(blank=True, db_column='DEPT_NAME', max_length=100, null=True)),
                ('resp_dept_code', models.CharField(blank=True, db_column='RESP_DEPT_CODE', max_length=5, null=True)),
                ('resp_dept_name', models.CharField(blank=True, db_column='RESP_DEPT_NAME', max_length=100, null=True)),
                ('manager_title', models.CharField(blank=True, db_column='MANAGER_TITLE', max_length=100, null=True)),
                ('manager_ext', models.CharField(blank=True, db_column='MANAGER_EXT', max_length=100, null=True)),
                ('manager_name', models.CharField(blank=True, db_column='MANAGER_NAME', max_length=100, null=True)),
                ('manager_code', models.CharField(blank=True, db_column='MANAGER_CODE', max_length=20, null=True)),
                ('note', models.CharField(blank=True, db_column='NOTE', max_length=200, null=True)),
                ('city_name', models.CharField(blank=True, db_column='CITY_NAME', max_length=100, null=True)),
                ('city_code', models.CharField(blank=True, db_column='CITY_CODE', max_length=20, null=True)),
                ('branch_name', models.CharField(blank=True, db_column='BRANCH_NAME', max_length=100, null=True)),
                ('branch_code', models.IntegerField(blank=True, db_column='BRANCH_CODE', null=True)),
            ],
            options={
                'db_table': 'apf_dept_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createddate', models.DateTimeField(blank=True, db_column='CreatedDate', null=True)),
            ],
            options={
                'db_table': 'project_members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectid', models.IntegerField(db_column='ProjectId')),
                ('taskid', models.IntegerField(db_column='TaskId')),
                ('actionname', models.IntegerField(db_column='ActionName')),
                ('actiondate', models.IntegerField(db_column='ActionDate')),
                ('notes', models.IntegerField(db_column='Notes')),
            ],
            options={
                'db_table': 'task_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VDeptsheetsdata',
            fields=[
                ('id', models.IntegerField(db_column='Id', primary_key=True, serialize=False)),
                ('deptcode', models.IntegerField(blank=True, db_column='DeptCode', null=True)),
                ('deptname', models.CharField(blank=True, db_column='DeptName', max_length=200, null=True)),
                ('mangerid', models.CharField(blank=True, db_column='MangerID', max_length=45, null=True)),
                ('empname', models.CharField(blank=True, db_column='EmpName', max_length=255, null=True)),
                ('totaltask', models.BigIntegerField(db_column='TotalTask')),
                ('done', models.BigIntegerField(blank=True, db_column='Done', null=True)),
                ('inprogress', models.BigIntegerField(blank=True, db_column='INPROGRESS', null=True)),
                ('notcomplete', models.BigIntegerField(blank=True, db_column='NOTCOMPLETE', null=True)),
                ('new', models.BigIntegerField(blank=True, db_column='NEW', null=True)),
            ],
            options={
                'db_table': 'v_deptsheetsdata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VFollowup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskname', models.CharField(blank=True, db_column='taskName', max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('assignedto', models.IntegerField(blank=True, db_column='AssignedTo', null=True)),
                ('projectid', models.IntegerField(blank=True, db_column='projectId', null=True)),
                ('projectname', models.CharField(blank=True, db_column='projectName', max_length=250, null=True)),
                ('empname', models.CharField(blank=True, db_column='EmpName', max_length=255, null=True)),
                ('deptcode', models.CharField(blank=True, db_column='DeptCode', max_length=45, null=True)),
                ('deptname', models.CharField(blank=True, db_column='DeptName', max_length=200, null=True)),
            ],
            options={
                'db_table': 'v_followup',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VSheetsdata',
            fields=[
                ('id', models.IntegerField(db_column='Id', primary_key=True, serialize=False)),
                ('employeeid', models.CharField(blank=True, db_column='EmployeeId', max_length=45, null=True)),
                ('employeename', models.CharField(blank=True, db_column='EmployeeName', max_length=255, null=True)),
                ('deptname', models.CharField(blank=True, db_column='DeptName', max_length=200, null=True)),
                ('deptcode', models.CharField(blank=True, db_column='DeptCode', max_length=45, null=True)),
                ('managername', models.CharField(blank=True, db_column='ManagerName', max_length=255, null=True)),
                ('totaltask', models.BigIntegerField(db_column='TotalTask')),
                ('notsubmitted', models.BigIntegerField(blank=True, db_column='NotSubmitted', null=True)),
                ('submitted', models.BigIntegerField(blank=True, db_column='Submitted', null=True)),
                ('new', models.BigIntegerField(blank=True, db_column='New', null=True)),
            ],
            options={
                'db_table': 'V_SheetsData',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VStatisticstaskdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectid', models.IntegerField(db_column='ProjectId')),
                ('proid', models.IntegerField(db_column='proID')),
                ('employeeid', models.CharField(blank=True, db_column='EmployeeId', max_length=45, null=True)),
                ('employeename', models.CharField(blank=True, db_column='EmployeeName', max_length=255, null=True)),
                ('jobtitle', models.CharField(blank=True, db_column='JobTitle', max_length=200, null=True)),
                ('deptname', models.CharField(blank=True, db_column='DeptName', max_length=200, null=True)),
                ('deptcode', models.CharField(blank=True, db_column='DeptCode', max_length=45, null=True)),
                ('managername', models.CharField(blank=True, db_column='ManagerName', max_length=255, null=True)),
                ('totaltask', models.BigIntegerField(blank=True, db_column='TotalTask', null=True)),
                ('new', models.BigIntegerField(blank=True, db_column='New', null=True)),
                ('inprogress', models.BigIntegerField(blank=True, db_column='Inprogress', null=True)),
                ('done', models.BigIntegerField(blank=True, db_column='Done', null=True)),
                ('closed', models.BigIntegerField(blank=True, db_column='Closed', null=True)),
                ('cancelled', models.BigIntegerField(blank=True, db_column='Cancelled', null=True)),
            ],
            options={
                'db_table': 'v_statisticstaskdata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalTask',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('projectid', models.IntegerField(db_column='ProjectId')),
                ('name', models.CharField(blank=True, db_column='Name', max_length=100, null=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=2500, null=True)),
                ('startdate', models.DateTimeField(blank=True, db_column='StartDate', null=True)),
                ('enddate', models.DateTimeField(blank=True, db_column='EndDate', null=True)),
                ('departementid', models.IntegerField(blank=True, db_column='DepartementId', null=True)),
                ('assignedto', models.IntegerField(blank=True, db_column='AssignedTo', null=True)),
                ('status', models.CharField(blank=True, choices=[('', 'Choice action'), ('New', 'New'), ('InProgress', 'InProgress'), ('Done', 'Done'), ('Hold', 'Hold'), ('Cancelled', 'Cancelled'), ('Closed', 'Closed')], db_column='Status', max_length=10, null=True)),
                ('assigneddate', models.DateTimeField(blank=True, db_column='AssignedDate', null=True)),
                ('realstartdate', models.DateTimeField(blank=True, db_column='RealStartDate', null=True)),
                ('realstartby', models.IntegerField(blank=True, db_column='RealStartBy', null=True)),
                ('finishedby', models.IntegerField(blank=True, db_column='FinishedBy', null=True)),
                ('finisheddate', models.DateTimeField(blank=True, db_column='FinishedDate', null=True)),
                ('cancelledby', models.IntegerField(blank=True, db_column='Cancelledby', null=True)),
                ('cancelleddate', models.DateTimeField(blank=True, db_column='CancelledDate', null=True)),
                ('closedby', models.IntegerField(blank=True, db_column='ClosedBy', null=True)),
                ('closeddate', models.DateTimeField(blank=True, db_column='ClosedDate', null=True)),
                ('closereson', models.CharField(blank=True, db_column='CloseReson', max_length=500, null=True)),
                ('lasteditdate', models.DateTimeField(blank=True, db_column='LastEditDate', null=True)),
                ('lasteditby', models.IntegerField(blank=True, db_column='LastEditBy', null=True)),
                ('deleted', models.IntegerField(blank=True, db_column='Deleted', null=True)),
                ('createdby', models.IntegerField(blank=True, db_column='CreatedBy', null=True)),
                ('createddate', models.DateTimeField(blank=True, db_column='CreatedDate', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical task',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.DeleteModel(
            name='Employee1',
        ),
    ]
