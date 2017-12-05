from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Department(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='ManagerId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'department'

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
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    taskdate = models.DateField(_('task date'),db_column='TaskDate', blank=False, null=False)  # Field name made lowercase.
    editedate = models.DateTimeField(db_column='EditeDate', blank=True, null=True)  # Field name made lowercase.
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
    reason = models.CharField(db_column='Reason',choices=REASON_STATUS, max_length=1,blank=True, null=True)  # Field name made lowercase.
    submittedby = models.IntegerField(db_column='SubmittedBy', blank=True, null=True)  # Field name made lowercase.
    submitteddate = models.DateTimeField(db_column='SubmittedDate', blank=True, null=True)  # Field name made lowercase.

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

class VDeptsheetsdata(models.Model):
    id = models.IntegerField(db_column='Id',primary_key=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mangerid = models.CharField(db_column='MangerID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totaltask = models.BigIntegerField(db_column='TotalTask')  # Field name made lowercase.
    done = models.BigIntegerField(db_column='Done', blank=True, null=True)  # Field name made lowercase.
    inprogress = models.BigIntegerField(db_column='INPROGRESS', blank=True, null=True)  # Field name made lowercase.
    notcomplete = models.BigIntegerField(db_column='NOTCOMPLETE', blank=True, null=True)  # Field name made lowercase.
    new = models.BigIntegerField(db_column='NEW', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_deptsheetsdata'

class ApfDeptView(models.Model):
    id = models.IntegerField(db_column='Id',primary_key=True)  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    resp_dept_code = models.CharField(db_column='RESP_DEPT_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    resp_dept_name = models.CharField(db_column='RESP_DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    manager_title = models.CharField(db_column='MANAGER_TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    manager_ext = models.CharField(db_column='MANAGER_EXT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    manager_name = models.CharField(db_column='MANAGER_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    manager_code = models.CharField(db_column='MANAGER_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='NOTE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    city_name = models.CharField(db_column='CITY_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    city_code = models.CharField(db_column='CITY_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    branch_name = models.CharField(db_column='BRANCH_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    branch_code = models.IntegerField(db_column='BRANCH_CODE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'apf_dept_view'

class Task(models.Model):
    projectid = models.IntegerField(db_column='ProjectId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=2500, blank=True, null=True)  # Field name made lowercase.

    TASK_STATUS = (
        ('', _('Choice action')),
        ('New', _('New')),
        ('InProgress', _('InProgress')),
        ('Done', _('Done')),
        ('Hold', _('Hold')),
        ('Cancelled', _('Cancelled')),
        ('Closed', _('Closed')),
    )
    status = models.CharField(db_column='Status',max_length=10,choices=TASK_STATUS, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    departementid = models.IntegerField(db_column='DepartementId', blank=True, null=True)  # Field name made lowercase.
    assignedto = models.IntegerField(db_column='AssignedTo', blank=True, null=True)  # Field name made lowercase.
    status = models.ForeignKey('ProjectStatus', on_delete=models.SET_NULL, null=True)
    assigneddate = models.DateTimeField(db_column='AssignedDate', blank=True, null=True)  # Field name made lowercase.
    realstartdate = models.DateTimeField(db_column='RealStartDate', blank=True, null=True)  # Field name made lowercase.
    realstartby = models.IntegerField(db_column='RealStartBy', blank=True, null=True)  # Field name made lowercase.
    finishedby = models.IntegerField(db_column='FinishedBy', blank=True, null=True)  # Field name made lowercase.
    finisheddate = models.DateTimeField(db_column='FinishedDate', blank=True, null=True)  # Field name made lowercase.
    canceledby = models.IntegerField(db_column='CanceledBy', blank=True, null=True)  # Field name made lowercase.
    canceleddate = models.DateTimeField(db_column='CanceledDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.IntegerField(db_column='ClosedBy', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    closereson = models.CharField(db_column='CloseReson', max_length=500, blank=True, null=True)  # Field name made lowercase.
    lasteditdate = models.DateTimeField(db_column='LastEditDate', blank=True, null=True)  # Field name made lowercase.
    lasteditby = models.IntegerField(db_column='LastEditBy', blank=True, null=True)  # Field name made lowercase.
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
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    name_ar = models.CharField(db_column='Name_Ar', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'task_status'

class ProjectMembers(models.Model):
    project =  models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project_members'

class VFollowup(models.Model):
    taskname = models.CharField(db_column='taskName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=10, blank=True, null=True)
    assignedto = models.IntegerField(db_column='AssignedTo', blank=True, null=True)  # Field name made lowercase.
    projectname = models.CharField(db_column='projectName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_followup'