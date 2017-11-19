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


class ApIpCurrJobDataView(models.Model):
    empindex = models.AutoField(db_column='empIndex', primary_key=True)  # Field name made lowercase.
    employee_id = models.BigIntegerField(db_column='EMPLOYEE_ID', unique=True, blank=True, null=True)  # Field name made lowercase.
    emp_name = models.CharField(db_column='EMP_NAME', max_length=42, blank=True, null=True)  # Field name made lowercase.
    gvrmnt_start_date = models.CharField(db_column='GVRMNT_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    org_start_date = models.CharField(db_column='ORG_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    office_phone = models.CharField(db_column='OFFICE_PHONE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qual_code = models.IntegerField(db_column='QUAL_CODE', blank=True, null=True)  # Field name made lowercase.
    qual_desc = models.CharField(db_column='QUAL_DESC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qual_type = models.CharField(db_column='QUAL_TYPE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    qual_type_desc = models.CharField(db_column='QUAL_TYPE_DESC', max_length=17, blank=True, null=True)  # Field name made lowercase.
    action_code = models.IntegerField(db_column='ACTION_CODE', blank=True, null=True)  # Field name made lowercase.
    job_grade = models.CharField(db_column='JOB_GRADE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    job_no = models.IntegerField(db_column='JOB_NO', blank=True, null=True)  # Field name made lowercase.
    job_title = models.CharField(db_column='JOB_TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    job_step = models.CharField(db_column='JOB_STEP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    action_start_date = models.CharField(db_column='ACTION_START_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    action_text = models.CharField(db_column='ACTION_TEXT', max_length=26, blank=True, null=True)  # Field name made lowercase.
    action_no = models.IntegerField(db_column='ACTION_NO', blank=True, null=True)  # Field name made lowercase.
    action_date = models.CharField(db_column='ACTION_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    action_end_date = models.CharField(db_column='ACTION_END_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    basic_salary = models.IntegerField(db_column='BASIC_SALARY', blank=True, null=True)  # Field name made lowercase.
    transportation = models.IntegerField(db_column='TRANSPORTATION', blank=True, null=True)  # Field name made lowercase.
    grade_basic_salary = models.CharField(db_column='GRADE_BASIC_SALARY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    grade_sort_no = models.CharField(db_column='GRADE_SORT_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    category_code = models.IntegerField(db_column='CATEGORY_CODE', blank=True, null=True)  # Field name made lowercase.
    cat_descreption = models.CharField(db_column='CAT_DESCREPTION', max_length=19, blank=True, null=True)  # Field name made lowercase.
    sex_code = models.IntegerField(db_column='SEX_CODE', blank=True, null=True)  # Field name made lowercase.
    birth_date = models.CharField(db_column='BIRTH_DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    birth_place = models.CharField(db_column='BIRTH_PLACE', max_length=22, blank=True, null=True)  # Field name made lowercase.
    nationality = models.IntegerField(db_column='NATIONALITY', blank=True, null=True)  # Field name made lowercase.
    nat_descreption = models.CharField(db_column='NAT_DESCREPTION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    current_dept_code = models.IntegerField(db_column='CURRENT_DEPT_CODE', blank=True, null=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    working_dept_code = models.CharField(db_column='WORKING_DEPT_CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    manager_id = models.CharField(db_column='MANAGER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    authority_id = models.CharField(db_column='AUTHORITY_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    work_dept_name = models.CharField(db_column='WORK_DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.IntegerField(db_column='EMP_TYPE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ap_ip_curr_job_data_view'


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
    end = models.DateField()
    teamname = models.CharField(db_column='TeamName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=250, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId', blank=True, null=True)  # Field name made lowercase.
    statusid = models.IntegerField(db_column='StatusId', blank=True, null=True)  # Field name made lowercase.
    openby = models.CharField(db_column='OpenBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    opendate = models.DateTimeField(db_column='OpenDate', blank=True, null=True)  # Field name made lowercase.
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

    class Meta:
        managed = False
        db_table = 'project_status'


class Sheet(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    empid = models.BigIntegerField(db_column='EmpId', blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
<<<<<<< HEAD
    managerlevel2 = models.BigIntegerField(db_column='ManagerLevel2', blank=True, null=True)  # Field name made lowercase.
    managerlevel3 = models.BigIntegerField(db_column='ManagerLevel3', blank=True, null=True)  # Field name made lowercase.
    managerlevel4 = models.BigIntegerField(db_column='ManagerLevel4', blank=True, null=True)  # Field name made lowercase.
    taskdesc = models.CharField(_('Task Descreption'),db_column='TaskDesc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    TASK_STATUS = (
        ('m', _('Master')),
        ('h', _('Help')),
    )
    tasktype = models.CharField(_('Task type'), max_length=1, choices=TASK_STATUS, db_column='TaskType', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(_('Duration'),db_column='Duration',blank=True, null=True)  # Field name made lowercase.
=======
    taskdesc = models.CharField(db_column='TaskDesc', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tasktype = models.CharField(db_column='TaskType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration', blank=True, null=True)  # Field name made lowercase.
>>>>>>> c9da7b3a5d64f22602ec2abcc1ecc3019098be40
    createddate = models.DateField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    taskdate = models.DateField(_('task date'),db_column='TaskDate', blank=True, null=True)  # Field name made lowercase.
    editedate = models.DateField(db_column='EditeDate', blank=True, null=True)  # Field name made lowercase.
    ifsubmitted = models.IntegerField(db_column='IfSubmitted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sheet'


class Task(models.Model):
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
    name = models.IntegerField(db_column='Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task_status'
