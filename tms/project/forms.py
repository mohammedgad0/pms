from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import modelformset_factory
from .models import *
from django.forms import ModelForm, Textarea,TextInput,DateField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError


class TeamModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname
    
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control has-feedback-left',
                                   'placeholder': _('User Name')}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control has-feedback-left',
                                   'placeholder':_('Password')}))

class AddNewSheet(forms.Form):
    TaskDesc = forms.CharField(label=_("Task Descreption"),
               widget=forms.TextInput({'class': 'form-control','placeholder': 'وصف المهمة كامل'}))

    TaskType = forms.ChoiceField(choices=(('M', _('Master')), ('H', _('Help'))),label=_("Task type"),
                    widget=forms.Select({'class': 'form-control','placeholder':'task'}))
    Duration = forms.IntegerField(label=_("Duration"),
               widget=forms.NumberInput({'class': 'form-control','placeholder':'0'}))

UpdateSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration'))

class FilterSheet(forms.Form):
    tasktype = forms.ChoiceField(choices=(("", _('')),('M', _('Master')), ('H', _('Help'))),label=_("Task type"),required=False,
                    widget=forms.Select({'class': 'form-control','placeholder':'task'}))
    tasksubmitted= forms.ChoiceField(choices=(
        ("", _('')),
        ('0', _('New')),
        ('1', _('submitted')),
        ('2', _('not submitted')),
    ),required=False,label=_("Status submitted"),widget=forms.Select({'class': 'form-control cust','placeholder':'task'}))
    taskstatus= forms.ChoiceField(choices=(
    ("", _('')),
        ('1', _('in progres')),
        ('2', _('Done')),
        ('3', _('Ignore')),
    ),required=False,label=_("Status task"),widget=forms.Select({'class': 'form-control','placeholder':'task'}))

class SheetForm(ModelForm):
    model = Sheet

class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['status'].empty_label = None
        self.fields['name'].widget.attrs['maxlength'] =255
        self.fields['delegationto'].empty_label = _("Select Employee")
     #fields   
    delegationto = TeamModelChoiceField(queryset=Employee.objects.all(),to_field_name="empid" ,
                     empty_label=_("Select Employee"),
                     widget=forms.Select(attrs={'class': 'chosen form-control col-md-3'} ),
                     label=_("Delegation To"),
                     required=False,help_text="تفويض إدارة المشروع الى موظف آخر",
                     )

    class Meta:
        model = Project
        fields = ['name','start','status','end','desc','delegationto']

       # status = models.ForeignKey(ProjectStatus, widget=forms.Select({'class': 'form-control','placeholder':'task'}) )
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Project Name'),'required': True}),
            'start':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'end':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
            'desc': Textarea(attrs={'class':'form-control','placeholder':_('Project Details'),'required': True}),
            'status':forms.Select(attrs={'class': 'form-control','placeholder':_('Select Status')}),
        }
        labels = {
            'name': _('Project Name'),
            'status': _('Status'),
            'start':_('Start Date'),
            'end':_('End Date'),
            'desc':_('Project Description'),
        }
        help_texts = {
            'desc': _('write a Description for Project .'),
            'start':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
            'end':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Project's name is too long."),
                    'required': _("Project's name is required."),
             },
            'start': {
                    'required': _("Start Date  is required."),
             },
            'end': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Project's Description is too long."),
                    'required': _("Description is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        end = cleaned_data.get("end")
        start = cleaned_data.get("start")
        #Check end date less than start date
        if end < start:
            msg = _("End date is less than start date")
            self.add_error('end', msg)
            
class EmployeeList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.empname

class DepartmentList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.deptname

class AddTaskForm(ModelForm):
    CHOICES = (('1', _('Employee'),), ('2', _('Department'),))
    employee = EmployeeList(queryset=Employee.objects.all(),to_field_name="empid",empty_label=_("Select Employee"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    department_list = DepartmentList(queryset=Department.objects.all(),to_field_name="deptcode",empty_label=_("Select Departement"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    assigntype = forms.ChoiceField(label=_('Assignto'),required=False,widget=forms.RadioSelect(attrs={'class':'form-check-input-task'}), choices=CHOICES)

    class Meta:
        model = Task
        fields = ['name','desc','assigntype',
        'employee',
        'department_list','startdate','enddate']
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Task Name'),'required': True}),
            'desc': Textarea(attrs={'id':'summernote','class':'form-control','placeholder':_('Task Details'),'required': True}),
            'startdate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'enddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
        }

        labels = {
            'name': _('Task Name'),
            'desc':_('Task Description'),
            'assigntype':_('Assignto'),
            'startdate':_('Start Date'),
            'enddate':_('End Date'),
        }
        help_texts = {
            'desc': _('write a Description for task .'),
            'startdate':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
            'enddate':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Project's name is too long."),
                    'required': _("Project's name is required."),
             },
            'startdate': {
                    'required': _("Start Date  is required."),
             },
            'enddate': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Task's Description is too long."),
                    'required': _("Description is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        enddate = cleaned_data.get("enddate")
        startdate = cleaned_data.get("startdate")
        #Check end date less than start date
        if enddate < startdate:
            msg = _("End date is less than start date")
            self.add_error('enddate', msg)

class EditTaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['maxlength'] =255

    CHOICES = (('1', _('Employee'),), ('2', _('Department'),))
    createdby = EmployeeList(queryset=Employee.objects.all(),to_field_name="empid", empty_label="(Nothing)",required=False,widget=forms.Select(attrs={'class': 'chosen form-control'} ))
    department_list = DepartmentList(queryset=Department.objects.all(),to_field_name="deptcode", empty_label=_("Select Departement"),required=False,widget=forms.Select(attrs={'class': 'chosen form-control','disabled':'disabled'} ))
    assigntype = forms.ChoiceField(label=_('Assignto'),required=False,widget=forms.RadioSelect(attrs={'class':'form-check-input-task'}), choices=CHOICES)
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':_("Note"),'placeholder':_("Note"), 'rows':'3','size': '40','required': 'True'}),required=False, max_length=250, error_messages={'required': 'note'})
    progress = forms.IntegerField(validators=[ MaxValueValidator(100, message="Progress Over 100"),MinValueValidator(0, message="Progress less 0")],min_value=0, max_value=100)
    assigned_to=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_('Responsible'),'required': False,}),required=False)
    class Meta:
        model = Task
        fields = ['name','desc','startdate','enddate','finisheddate','assigntype','status','progress']
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Task Name'),'required': True}),
            'desc': Textarea(attrs={ 'id':'summernote','class':'form-control ','placeholder':_('Task Details'),'required': True}),
            'startdate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': False}),
            'enddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': False}),
            'finisheddate':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_3','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': False}),
            'assignedto':TextInput(attrs={'class': 'form-control','placeholder':_('Responsible'),'required': False,}),
            'progress': forms.NumberInput(attrs={'class': 'form-control','placeholder':_('Progress'),'required': False,'min': 0, 'max': 100 }),
            'status':forms.Select(attrs={'class': 'form-control','placeholder':_('Select Status')})

        }
        labels = {
            'name': _('Task Name'),
            'desc':_('Task Description'),
            'assigntype':_('Assignto'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Task's name is too long."),
                    'required': _("Task's name is required."),
             },
            'startdate': {
                    'required': _("Start Date  is required."),
             },
            'enddate': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Task's Description is too long."),
                    'required': _("Description is required."),
             },
            'progress': {
                    'MaxValueValidator': _("The Task's Pogress is over rang 100."),
                    'MinValueValidator': _("Task's name is less than 0."),
             },
            'status': {
                    'required': _("Status is required."),
             },

        }
    def clean(self):
        cleaned_data = super().clean()
        enddate = cleaned_data.get("enddate")
        startdate = cleaned_data.get("startdate")
        #Check end date less than start date
        if enddate < startdate:
            msg = _("End date is less than start date")
            self.add_error('enddate', msg)

class TaskStartForm(forms.Form):
       rsd = forms.DateField(label=_("Real Start Date"),
       widget=forms.DateInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Real Start Date'),'required': True}))
       notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':'Notes', 'size': '40','required': False}), required=False,error_messages={'required': 'note'},label=_('Note'))

class TaskFinishForm(forms.Form):
       ftime = forms.DateField(label=_("Finished on"),
       widget=forms.DateInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Finished Date'),'required': True}))
       notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':'Notes', 'size': '40','required': False}), required=False,error_messages={'required': 'notes'},label=_('Note'))

class TaskCloseForm(forms.Form):
       ctime = forms.DateField(label=_("Closed on"),required=False,
       widget=forms.DateInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Closed on Date'),'required': False}))
       reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':_("Please enter a reason to Close "), 'size': '40','required': True}),required=True, max_length=500, error_messages={'required': _('Reason')},label=_("Reason"))

class TaskProgressForm(ModelForm):
      progress = forms.IntegerField(validators=[ MaxValueValidator(100, message="Progress Over 100"),MinValueValidator(0, message="Progress less 0")],min_value=0, max_value=100,label=_('Progress'))
      note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':'Notes', 'size': '40','required': False}), required=False,error_messages={'required': 'notes'},label=_('Note'))

      class Meta:
        model = Task
        fields = ['progress']
        widgets = {
            'progress': forms.NumberInput(attrs={'class': 'form-control','placeholder':_('Progress'),'required': False,'min': 0, 'max': 100 })

        }
        labels = {
            'progress': _('Task Progress'),

        }
        error_messages = {

            'progress': {
                    'MaxValueValidator': _("The Task's Pogress is over rang 100."),
                    'MinValueValidator': _("Task's name is less than 0."),
             },


        }

class TaskCancelForm(forms.Form):
       reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','label':_("Reason"),'placeholder':_("Please enter a reason to cancel"), 'size': '40','required': 'True'}),required=True, max_length=500, error_messages={'required':  _('Reason')},label=_('Reason'))

class TaskPauseForm(forms.Form):
       note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'size': '40','required': 'True'}),required=True, max_length=500, error_messages={'required': 'note'},label=_('Note'))



class FollowupModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.deptname

class TeamForm(forms.Form):
      employee = TeamModelChoiceField(queryset=Employee.objects.all(), empty_label=_("Select Employee"),widget=forms.Select(attrs={'class': 'chosen'} ))

class TaskAssignToForm(forms.Form):
      CHOICES=CHOICES=[('emp',_('Employee')),('dept',_('Departement'))]
      assigntype =forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class':''}),initial="emp",label=_('Assign Type'))
      employee = TeamModelChoiceField(queryset=Employee.objects.none(),to_field_name="empid" ,empty_label=_("Select Employee"),widget=forms.Select(attrs={'class': 'chosen form-control col-md-8'} ),required=True,error_messages={'required': _('Select Employee')},label=_('Employee'))
      departement = FollowupModelChoiceField(queryset=Department.objects.all(), to_field_name="deptcode",empty_label=_("Select Departement"),widget=forms.Select(attrs={'class': 'chosen  form-control col-md-3',} ),error_messages={'required': _('Select Departement')},required=True,label=_('Departement'))

class FollowupForm(forms.Form):
      departement=[]
      query = VFollowup.objects.all()
      for data in query:
          if data.deptcode == None or data.deptcode == '' or data.deptcode == 'null':
              continue
          departement.append(data.deptcode)  
      departement = FollowupModelChoiceField(queryset=Department.objects.filter(deptcode__in= departement), to_field_name="deptcode",empty_label=_('Select Departement'),widget=forms.Select(attrs={'class': 'chosen chosen form-control col-md-3'} ),error_messages={'required': _('Please Sealect Departement')},label=_('Departement'))
      employee = TeamModelChoiceField(queryset=Employee.objects.none(),to_field_name="empid" ,empty_label=_("Select Employee"),widget=forms.Select(attrs={'class': 'chosen form-control col-md-3'} ),required=False,label=_('Employee'))
      TASK_STATUS = (
        ('', _('Choice action')),
        ('New', _('New')),
        ('InProgress', _('InProgress')),
        ('Done', _('Done')),
        ('Hold', _('Hold')),
        ('Cancelled', _('Cancelled')),
        ('Closed', _('Closed')),
        )
      taskstatus= forms.ChoiceField(choices=TASK_STATUS,required=False,label=_("Status"),widget=forms.Select(attrs={'class': ' form-control col-md-3 chosen'}) )

class UploadFile(ModelForm):
    class Meta:
        model = Media
        fields = ['filepath','filename']
        labels = {
            'filename': _('File Name'),
            'filepath': _('Choose File'),

        }
class AddDelegation(ModelForm):
    employee = EmployeeList(queryset=Employee.objects.all(),to_field_name="empid",label=_("Delegation to"), empty_label=_("Nothing"),required=True,widget=forms.Select(attrs={'class': 'chosen form-control'} ))
    class Meta:
        model = Delegation
        fields = ['employee','start','end']
        widgets = {
            # 'authorized':TextInput(attrs={'class': 'form-control','placeholder':_('Employee name'),'required': True}),
            'start':TextInput(attrs={'class': 'form-control has-feedback-left col-md-3 col-sm-9 col-xs-12 ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'end':TextInput(attrs={'class': 'form-control has-feedback-left col-md-6 ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
        }
        labels = {
            'start':_('start Delegation'),
            'end':_('End Delegation'),
        },
    def clean(self):
        cleaned_data = super().clean()
        end = cleaned_data.get("end")
        start = cleaned_data.get("start")
        #Check end date less than start date
        if end < start:
            msg = _("End date is less than start date")
            self.add_error('end', msg)

class ProjectModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
class ApfDeptViewModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.dept_name
class ReportForm(forms.Form):
    RERPORT_TYPE_CHOICES = (('project', _('Project Summary')),('assignedto', _('Assignation')),('status', _('Status')),)
    departement = ApfDeptViewModelChoiceField(queryset=ApfDeptView.objects.none(), to_field_name="dept_code",empty_label=_('Select Departement'),widget=forms.Select(attrs={'class': 'chosen  form-control col-md-3',} ),error_messages={'required': _('Please Sealect Departement')},required=False)
    project =ProjectModelChoiceField(queryset=Project.objects.none(),to_field_name="id" ,empty_label=_('Select Project'),widget=forms.Select(attrs={'class': 'chosen form-control col-md-8'} ),required=True,error_messages={'required': _('Please Select Project')})
    reportType = forms.MultipleChoiceField( required=True,widget=forms.CheckboxSelectMultiple(attrs={'class': 'chektype'} ),choices=RERPORT_TYPE_CHOICES,
   error_messages={'required': _('Please Select Report Type')}
    )
