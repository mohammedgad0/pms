from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models



class ApDeptTab(models.Model):
    dept_code = models.IntegerField(db_column='DEPT_CODE', blank=True, null=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=86, blank=True, null=True)  # Field name made lowercase.
    branch_code = models.IntegerField(db_column='BRANCH_CODE', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='NOTE', max_length=21, blank=True, null=True)  # Field name made lowercase.
    manager_code = models.CharField(db_column='MANAGER_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manager_title = models.CharField(db_column='MANAGER_TITLE', max_length=105, blank=True, null=True)  # Field name made lowercase.
    manager_ext = models.CharField(db_column='MANAGER_EXT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    manager_phone = models.CharField(db_column='MANAGER_PHONE', max_length=9, blank=True, null=True)  # Field name made lowercase.
    resp_dept_code = models.CharField(db_column='RESP_DEPT_CODE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    manager_level = models.CharField(db_column='MANAGER_LEVEL', max_length=7, blank=True, null=True)  # Field name made lowercase.
    authority_a = models.CharField(db_column='AUTHORITY_A', max_length=50, blank=True, null=True)  # Field name made lowercase.
    authority_b = models.CharField(db_column='AUTHORITY_B', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ap_dept_tab'



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Department(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='ManagerId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    empid = models.CharField(db_column='EmpId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='IsManager', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=45, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class Project(models.Model):
    name = models.CharField(db_column='Name', max_length=250)  # Field name made lowercase.
    start = models.DateField(db_column='Start')  # Field name made lowercase.
    end = models.DateField(db_column='End')
    teamname = models.CharField(db_column='TeamName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=250)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId', blank=True, null=True)  # Field name made lowercase.
    #statusid = models.IntegerField(db_column='StatusId', blank=True, null=True)  # Field name made lowercase.
    status = models.ForeignKey('ProjectStatus', on_delete=models.SET_NULL, null=True)
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

class ProjectStatus(models.Model):
    name = models.IntegerField(db_column='Name')  # Field name made lowercase.
    name_ar = models.IntegerField(db_column='Name_Ar')  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority')  # Field priority made lowercase.
    isdefault = models.IntegerField(db_column='IsDefault')  # Field isdefault made lowercase.
    color = models.IntegerField(db_column='Color')  # Field color made lowercase.

    def __str__(self):
        return self.name_ar
        self.fields['verb'].empty_label = 'None'

    class Meta:
        managed = False
        db_table = 'project_status'


class Sheet(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    empid = models.BigIntegerField(db_column='EmpId', blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
    managerlevel2 = models.BigIntegerField(db_column='ManagerLevel2', blank=True, null=True)  # Field name made lowercase.
    managerlevel3 = models.BigIntegerField(db_column='ManagerLevel3', blank=True, null=True)  # Field name made lowercase.
    managerlevel4 = models.BigIntegerField(db_column='ManagerLevel4', blank=True, null=True)  # Field name made lowercase.
    taskdesc = models.CharField(_('Task Descreption'),db_column='TaskDesc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    TASK_STATUS = (
        ('', _('Choice type')),
        ('m', _('Master')),
        ('h', _('Help')),
    )
    tasktype = models.CharField(_('Task type'), max_length=1, choices=TASK_STATUS, db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(_('Duration'),db_column='Duration',blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    taskdate = models.DateField(_('task date'),db_column='TaskDate', blank=False, null=False)  # Field name made lowercase.
    editedate = models.DateField(db_column='EditeDate', blank=True, null=True)  # Field name made lowercase.
    SUBMITTED_STATUS = (
        ('', _('Choice action')),
        ('0', _('New')),
        ('1', _('submitted')),
        ('2', _('not submitted')),
    )
    ifsubmitted = models.CharField(db_column='IfSubmitted',max_length=1,choices=SUBMITTED_STATUS, blank=True, null=True)  # Field name made lowercase.
    SHEET_STATUS = (
    ('', _('Choice status')),
        ('0', _('New')),
        ('1', _('in progres')),
        ('2', _('Done')),
        ('3', _('Ignore')),
    )
    status = models.CharField(db_column='Status',choices=SHEET_STATUS, max_length=1)  # Field name made lowercase.
    statusdate = models.DateTimeField(db_column='StatusDate', blank=True, null=True)  # Field name made lowercase.
    REASON_STATUS = (
    ('', _('Choice reason')),
        ('0', _('Need Support')),
        ('1', _('Change piroty')),
    )
    reason = models.CharField(db_column='Reason',choices=REASON_STATUS, max_length=1)  # Field name made lowercase.
    submittedby = models.IntegerField(db_column='SubmittedBy', blank=True, null=True)  # Field name made lowercase.
    submitteddate = models.DateField(db_column='SubmittedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sheet'

class VSheetsdata(models.Model):
    id = models.IntegerField(db_column='Id',primary_key=True)  # Field name made lowercase.
    employeeid = models.CharField(db_column='EmployeeId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    employeename = models.CharField(db_column='EmployeeName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    managername = models.CharField(db_column='ManagerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totaltask = models.BigIntegerField(db_column='TotalTask')  # Field name made lowercase.
    notsubmitted = models.BigIntegerField(db_column='NotSubmitted', blank=True, null=True)  # Field name made lowercase.
    submitted = models.BigIntegerField(db_column='Submitted', blank=True, null=True)  # Field name made lowercase.
    new = models.BigIntegerField(db_column='New', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SheetsData'

class Task(models.Model):
    projectid = models.IntegerField(db_column='ProjectId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId', blank=True, null=True)  # Field name made lowercase.
    assignedto = models.IntegerField(db_column='AssignedTo', blank=True, null=True)  # Field name made lowercase.
    assigneddate = models.DateTimeField(db_column='AssignedDate', blank=True, null=True)  # Field name made lowercase.
    realstartdate = models.DateTimeField(db_column='RealStartDate', blank=True, null=True)  # Field name made lowercase.
    finishedby = models.IntegerField(db_column='FinishedBy', blank=True, null=True)  # Field name made lowercase.
    finisheddate = models.DateTimeField(db_column='FinishedDate', blank=True, null=True)  # Field name made lowercase.
    canceledby = models.IntegerField(db_column='CanceledBy', blank=True, null=True)  # Field name made lowercase.
    canceleddate = models.DateTimeField(db_column='CanceledDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.IntegerField(db_column='ClosedBy', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    closereson = models.CharField(db_column='CloseReson', max_length=500, blank=True, null=True)  # Field name made lowercase.
    lastedit = models.DateTimeField(db_column='LastEdit', blank=True, null=True)  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.
    createdby = models.IntegerField(db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task'


class TaskHistory(models.Model):
    projectid = models.IntegerField(db_column='ProjectId')  # Field name made lowercase.
    taskid = models.IntegerField(db_column='TaskId')  # Field name made lowercase.
    actionname = models.IntegerField(db_column='ActionName')  # Field name made lowercase.
    actiondate = models.IntegerField(db_column='ActionDate')  # Field name made lowercase.
    notes = models.IntegerField(db_column='Notes')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task_history'

class TaskStatus(models.Model):
    name = models.IntegerField(db_column='Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task_status'
