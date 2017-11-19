from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.views import *
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.forms import formset_factory
from .models import *
from django.forms import BaseModelFormSet
from datetime import datetime , timedelta

class BaseSheetFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseSheetFormSet, self).__init__(*args, **kwargs)
        empID = request.session['EmpID']
        self.queryset = Sheet.objects.filter(empid= 'empID')

def myuser(request, *args, **kwargs):
    if request.method == "POST":
        form = BootstrapAuthenticationForm(request, data=request.POST)
        emp = None
        if form.is_valid():
            auth_login(request, form.get_user())
            # email = None
            # if request.user.is_authenticated():
            email = request.user.email
            emp = Employee.objects.filter(email= email)
    # Get all data filtered by user email and set in session
        for data in emp:
            request.session['EmpID'] = data.empid
            request.session['EmpName'] = data.empname
            request.session['DeptName'] = data.deptname
            request.session['Mobile'] = data.mobile
            request.session['DeptCode'] = data.deptcode
    return login(request, *args, **kwargs)
# @login_required
def index(request):
    # Populate User From Ldap Without Login
    # from django_auth_ldap.backend import LDAPBackend
    # ldap_backend = LDAPBackend()
    # ldap_backend.populate_user('tgalharbi@stats.gov.sa')
    logged = request.COOKIES.get('logged_in_status')
    context = {'logged':logged}
    template = loader.get_template('project/index.html')
    return HttpResponse(template.render(context, request))
# request.session['idempresa'] = profile.idempresa

def gentella_html(request):
    context = {'LANG': request.LANGUAGE_CODE}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('project/' + load_template)
    return HttpResponse(template.render(context, request))

def MySheet(request):
    EmpID = 0
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    sheets = Sheet.objects.filter(empid = EmpID)
    context = {'AllSheets': sheets}
    return render(request, 'project/my_tasks.html', context)

def DeptSheet(request):
    DeptCode = 0
    EmpID = 0
    if request.user.is_authenticated():
        DeptCode = request.session['DeptCode']
        EmpID = request.session['EmpID']
    dept = Department.objects.filter(deptcode= DeptCode)[:1]
    managid = '0'
    sheets = None
    for data in dept:
        managid = data.managerid
    if managid == EmpID:
        # sheets = Sheet.objects.filter(deptcode = DeptCode)
        sheets = Sheet.objects.raw("SELECT sheet.TaskDesc, sheet.Id, EmpName FROM sheet INNER JOIN employee ON sheet.EmpId = employee.EmpId WHERE sheet.DeptCode =%s",  [DeptCode] )
    empdata = Employee.objects.all()
    context = {'AllSheets': sheets, 'department':dept, 'empid':EmpID, 'empdata':empdata}
    return render(request, 'project/dept_tasks.html', context)

# Add sheet form
# @login_required
def AddSheet(request):
    AddSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate'), extra=4,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control'}),
            'tasktype': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'taskdate': forms.TextInput(attrs={'class': 'datepicker form-control'}),
        }

    )
    EmpID = 0
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    formset = AddSheet(queryset=Sheet.objects.filter(empid= EmpID , ifsubmitted = '0',
    taskdate__gte=datetime.now()-timedelta(days=7), taskdate__lte=datetime.now()+ timedelta(days=7)
    ))
    if request.method == 'POST':
        formset = AddSheet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            # Get managers as hierarchicaly
            email = request.user.email
            emp = Employee.objects.filter(email= email)
            # managr level 1
            for data in emp:
                managercode = data.managercode
                request.session['MNGID'] = managercode
            # managr level 2
            emp1 = Employee.objects.filter(empid=managercode)
            for manager in emp1:
                 manager_2 = manager.managercode
            # managr level 3
            emp2 = Employee.objects.filter(empid=manager_2)
            for manager in emp2:
                 manager_3 = manager.managercode
            # managr level 4
            emp3 = Employee.objects.filter(empid=manager_3)
            for manager in emp3:
                 manager_4 = manager.managercode
            for obj in instances:
                obj.empid = request.session['EmpID']
                obj.deptcode = request.session['DeptCode']
                obj.managercode = managercode
                obj.managerlevel2 = manager_2
                obj.managerlevel3 = manager_3
                obj.managerlevel4 = manager_4
                obj.ifsubmitted = '0'
                if obj.createddate:
                    obj.editedate = datetime.now()
                else:
                    obj.createddate = datetime.now()
                obj.save()
    else:
        formset = formset
    # form = form_class(request.POST or None)
    return render(request, 'project/add-sheet.html', {'form': formset})

def AddProject(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ProjectName = form.cleaned_data['ProjectName']
            StartDate = form.cleaned_data['StartDate']
            EndDate = form.cleaned_data['EndDate']
            Desc = form.cleaned_data['Desc']
<<<<<<< HEAD
            p_obj= Project(name=ProjectName,start=StartDate,end=EndDate,desc=Desc,createddate=datetime.now())
            p_obj.save()
=======
            #collect datat into form model 
            Project_Object=  Project(id,name=ProjectName,start=StartDate,end=EndDate,desc=Desc)
            #save to database
            Project_Object.save()
>>>>>>> b5bc0782fca1bfda8e9c7ef3a425f504d1e390f4
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project/add_project.html', {'form': form})
