from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator

class Department(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True, unique=True)  # Field name made lowercase.
    managerid = models.CharField(db_column='ManagerId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.IntegerField(db_column='DeptCode', unique=True, blank=True, null=True)  # Field name made lowercase.
    managername = models.CharField(db_column='ManagerName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'department'

class Employee(models.Model):
    empid = models.IntegerField(db_column='EmpId', unique=True)  # Field name made lowercase.
    empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ismanager = models.IntegerField(db_column='IsManager', blank=True, null=True)  # Field name made lowercase.
    ext = models.CharField(db_column='Ext', max_length=45, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.
    managercode = models.BigIntegerField(db_column='ManagerCode', blank=True, null=True)  # Field name made lowercase.
    sexcode = models.CharField(db_column='SexCode', max_length=6, blank=True, null=True)  # Field name made lowercase.
    iscontract = models.IntegerField(db_column='IsContract', blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'employee'

class Project(models.Model):
    name = models.CharField(db_column='Name', max_length=250)  # Field name made lowercase.
    start = models.DateField(db_column='Start')  # Field name made lowercase.
    end = models.DateField(db_column='End')
    teamname = models.CharField(db_column='TeamName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=1500)  # Field name made lowercase.
    #createdby = models.CharField(db_column='CreatedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    createdby = models.ForeignKey('Employee',db_column='createdby',to_field='empid',related_name='Employee_createdby',on_delete=models.SET_NULL, blank=True, null=True)

    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    departement = models.ForeignKey('Department',db_column='DepartementId', to_field='deptcode',on_delete=models.SET_NULL, blank=True, null=True)
    #statusid = models.IntegerField(db_column='StatusId', blank=True, null=True)  # Field name made lowercase.
    status = models.ForeignKey('ProjectStatus', on_delete=models.SET_NULL, null=True)
    openedby = models.CharField(db_column='OpenedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    openeddate = models.DateTimeField(db_column='OpenedDate', blank=True, null=True)  # Field name made lowercase.
    closedby = models.CharField(db_column='ClosedBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    canceledby = models.CharField(db_column='CanceledBy', max_length=20, blank=True, null=True)  # Field name made lowercase.
    canceleddate = models.DateTimeField(db_column='CanceledDate', blank=True, null=True)  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.
    lasteditby = models.ForeignKey('Employee',db_column='LastEditBy',to_field='empid',related_name='Project_Employee_LastEditBy',on_delete=models.SET_NULL, blank=True, null=True)
    delegationto = models.ForeignKey('Employee',db_column='DelegationTo',to_field='empid',related_name='Project_Employee_DelegationTo',on_delete=models.SET_NULL, blank=True, null=True)
    delegationdate= models.DateTimeField(db_column='DelegationDate', blank=True, null=True) 
    class Meta:
        managed = False
        db_table = 'project'

class ProjectStatus(models.Model):
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    name_ar = models.CharField(db_column='Name_Ar', max_length=10)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority')  # Field name made lowercase.
    isdefault = models.IntegerField(db_column='IsDefault')  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=10)  # Field name made lowercase.

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
    dept_code = models.CharField(db_column='DEPT_CODE', max_length=5, blank=True, null=True,unique=True)  # Field name made lowercase.
    dept_name = models.CharField(db_column='DEPT_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
   # resp_dept_code = models.CharField(db_column='RESP_DEPT_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
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
    resp_dept_code = models.ForeignKey('self',db_column='resp_dept_code', to_field='dept_code',on_delete=models.SET_NULL, blank=True, null=True)
    
    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in ApfDeptView.objects.filter(resp_dept_code=self):
            _r = c.get_all_children(include_self=True)
            if 0 < len(_r):
                r.extend(_r)
        return r

    class Meta:
        managed = False
        db_table = 'apf_dept_view'

class Task(models.Model):
    assignedto = models.ForeignKey('Employee',db_column='assignedto',to_field='empid',related_name='Emp3', on_delete=models.SET_NULL, blank=True, null=True)
    departement = models.ForeignKey('Department',db_column='departementid', to_field='deptcode',on_delete=models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey('Project',db_column='projectid', to_field='id', on_delete=models.SET_NULL,blank=True,  null=True)

    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    desc = models.CharField(db_column='Desc', max_length=2500)  # Field name made lowercase.

    TASK_STATUS = (
        ('', _('Choice action')),
        ('New', _('New')),
        ('InProgress', _('InProgress')),
        ('Done', _('Done')),
        ('Hold', _('Hold')),
        ('Cancelled', _('Cancelled')),
        ('Closed', _('Closed')),
    )
    status = models.CharField(db_column='Status',max_length=10,choices=TASK_STATUS, blank=False, null=False)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.

    assigneddate = models.DateTimeField(db_column='AssignedDate', blank=True, null=True)  # Field name made lowercase.
    progress = models.PositiveSmallIntegerField(blank=True, null=True)
    realstartdate = models.DateTimeField(db_column='RealStartDate', blank=True, null=True)  # Field name made lowercase.
    realstartby = models.IntegerField(db_column='RealStartBy', blank=True, null=True)  # Field name made lowercase.
    finishedby = models.IntegerField(db_column='FinishedBy', blank=True, null=True)  # Field name made lowercase.
    finisheddate = models.DateTimeField(db_column='FinishedDate', blank=True, null=True)  # Field name made lowercase.
    cancelledby = models.IntegerField(db_column='CancelledBy', blank=True, null=True)  # Field name made lowercase.
    cancelleddate = models.DateTimeField(db_column='CancelledDate', blank=True, null=True)  # Field name made lowercase.
    cancellreson = models.CharField(db_column='CancellReson', max_length=500, blank=True, null=True)  # Field name made lowercase.
    closedby = models.IntegerField(db_column='ClosedBy', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    closereson = models.CharField(db_column='CloseReson', max_length=500, blank=True, null=True)  # Field name made lowercase.
    deleted = models.IntegerField(db_column='Deleted', blank=True, null=True)  # Field name made lowercase.
    createdby = models.ForeignKey('Employee',to_field='empid',related_name='Emp4',db_column='CreatedBy', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    lasteditdate = models.DateTimeField(db_column='LastEditDate', blank=True, null=True)  # Field name made lowercase.
    lasteditby =models.ForeignKey('Employee',to_field='empid',related_name='Task_Employee_LastEditBy',db_column='LastEditBy', blank=True, null=True)

    history = HistoricalRecords()
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

# class ProjectMembers(models.Model):
#     project =  models.ForeignKey(Project, on_delete=models.CASCADE)
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'project_members'

class VFollowup(models.Model):
     taskname = models.CharField(db_column='taskName', max_length=100, blank=True, null=True)  # Field name made lowercase.
     status = models.CharField(max_length=10, blank=True, null=True)
     assignedto = models.IntegerField(db_column='AssignedTo', blank=True, null=True)  # Field name made lowercase.
     projectid = models.IntegerField(db_column='projectId', blank=True, null=True)  # Field name made lowercase.
     projectname = models.CharField(db_column='projectName', max_length=250, blank=True, null=True)  # Field name made lowercase.
     empname = models.CharField(db_column='EmpName', max_length=255, blank=True, null=True)  # Field name made lowercase.
     deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
     deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.

     class Meta:
        managed = False
        db_table = 'v_followup'

class VStatisticstaskdata(models.Model):
    projectid = models.IntegerField(db_column='ProjectId')  # Field name made lowercase.
    employeeid = models.CharField(db_column='EmployeeId', max_length=45, blank=True, null=True)  # Field name made lowercase.
    employeename = models.CharField(db_column='EmployeeName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='DeptCode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    managername = models.CharField(db_column='ManagerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    totaltask = models.BigIntegerField(db_column='TotalTask', blank=True, null=True)  # Field name made lowercase.
    new = models.BigIntegerField(db_column='New', blank=True, null=True)  # Field name made lowercase.
    inprogress = models.BigIntegerField(db_column='Inprogress', blank=True, null=True)  # Field name made lowercase.
    done = models.BigIntegerField(db_column='Done', blank=True, null=True)  # Field name made lowercase.
    closed = models.BigIntegerField(db_column='Closed', blank=True, null=True)  # Field name made lowercase.
    cancelled = models.BigIntegerField(db_column='Cancelled', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_statisticstaskdata'

class Media(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    project = models.ForeignKey('Project',db_column='projectid',to_field='id', on_delete=models.SET_NULL, blank=True, null=True)
    task = models.ForeignKey('Task',db_column='taskid',to_field='id', on_delete=models.SET_NULL, blank=True, null=True)
    filename = models.CharField(blank=True,null=True, max_length=100)
    filepath = models.FileField(_('Files Upload'),upload_to='documents/',blank=True, null=True)
    class Meta:
        db_table = 'media'

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Media)
def Media_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
     instance.delete()

class Delegation(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)  # Field name made lowercase.
    managerid = models.ForeignKey('Employee', db_column='ManagerId', to_field='empid',related_name='Emp1',blank=True, null=True)  # Field name made lowercase.
    deptcode = models.ForeignKey('Department',to_field='deptcode', db_column='DeptCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    authorized = models.ForeignKey('Employee',to_field='empid',related_name='Emp2', db_column='Authorized', blank=True, null=True)  # Field name made lowercase.
    deptauthcode = models.CharField(db_column='DeptAuthCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    start = models.DateTimeField(db_column='Start', blank=True, null=True)  # Field name made lowercase.
    end = models.DateTimeField(db_column='End', blank=True, null=True)  # Field name made lowercase.
    expired = models.CharField(db_column='Expired', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'delegation'


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
           
