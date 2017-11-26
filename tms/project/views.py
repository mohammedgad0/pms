from django.shortcuts import render, render_to_response ,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect,Http404 ,HttpResponseForbidden
from .models import *
from .forms import *
from django.contrib.auth.views import *
from django.utils.translation import ugettext as _
from django.forms import formset_factory
from django.forms import BaseModelFormSet
from datetime import datetime , timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required


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
        if request.user.is_authenticated():
            email = request.user.email
            emp = Employee.objects.filter(email= email)
        # Get all data filtered by user email and set in session
            for data in emp:
                request.session['EmpID'] = data.empid
                request.session['EmpName'] = data.empname
                request.session['DeptName'] = data.deptname
                request.session['Mobile'] = data.mobile
                request.session['DeptCode'] = data.deptcode
                request.session['JobTitle'] = data.jobtitle
                request.session['IsManager'] = data.ismanager
            if emp:
                if data.ismanager == 1:
                    g = Group.objects.get(name='ismanager')
                    g.user_set.add(request.user.id)
                else:
                    g = Group.objects.get(name='employee')
                    g.user_set.add(request.user.id)
            # if not emp:
            #     g = Group.objects.get(name='employee')
            #     g.user_set.add(request.user.id)

        else:
            return login(request, *args, **kwargs)
    return login(request, *args, **kwargs)

@login_required
def index(request):
    # if request.user.is_authenticated():
    #     email = request.user.email
    #     emp = Employee.objects.filter(email= email)
    # # Get all data filtered by user email and set in session
    #     for data in emp:
    #         request.session['EmpID'] = data.empid
    #         request.session['EmpName'] = data.empname
    #         request.session['DeptName'] = data.deptname
    #         request.session['Mobile'] = data.mobile
    #         request.session['DeptCode'] = data.deptcode
    # Populate User From Ldap Without Login
    # from django_auth_ldap.backend import LDAPBackend
    # ldap_backend = LDAPBackend()
    # ldap_backend.populate_user('aalmanie@stats.gov.sa')
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

@login_required
#@permission_required('project.add_sheet',raise_exception=True)
def MySheet(request):

    EmpID = 0
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    sheets = Sheet.objects.filter(empid = EmpID).order_by('ifsubmitted')
    count = len(list(sheets))
    if count == 0:
        messages.info(request, _("No tasks"))
    context = {'AllSheets': sheets,'count':count}
    return render(request, 'project/my_tasks.html', context)

@login_required
def ManagerPage(request):
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
    # if this user is manager
    AllEmp = "0"
    if managid == EmpID:
        AllEmp = VSheetsdata.objects.filter(deptcode = DeptCode).order_by('new')
        # AllEmp = Sheet.objects.raw('''SELECT sheet.Id, EmpName as employee, COUNT(sheet.Id) as Tasks ,
        #                             (select count(sheet.IfSubmitted) from sheet where IfSubmitted=0
        #                             and EmpId = employee.EmpId) as notsubmitted,
        #                             (select count(sheet.IfSubmitted) from sheet where IfSubmitted=1
        #                             and EmpId = employee.EmpId) as submitted
        #                             FROM sheet
        #                             INNER JOIN employee
        #                             ON sheet.EmpId = employee.EmpId
        #                             WHERE sheet.DeptCode = %s'' group by EmpName''' , [DeptCode])
    # for data in AllEmp:
    count = len(list(AllEmp))
    if count == 0:
        messages.info(request, _("No data"))
        return render(request, 'project/all_sheets.html')
    context = {'allemp':AllEmp,"count":count}
    return render(request, 'project/all_sheets.html',context)

def AllSheets(request):
    AllEmp = VSheetsdata.objects.filter()
    query = request.GET.get("q")
    if query:
        AllEmp = VSheetsdata.objects.filter(
        Q(employeeid__icontains = query)|
        Q(employeename__icontains = query)|
        Q(deptname__icontains = query)
        )
    # for data in AllEmp:
    count = len(list(AllEmp))
    if count == 0:
        messages.info(request, _("No data there"))
        return render(request, 'project/all_emp_sheets.html')
    context = {'allemp':AllEmp,"count":count}
    return render(request, 'project/all_emp_sheets.html',context)

@login_required
def UpdateSheet(request,empid):
    SbmitSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate','ifsubmitted'), extra=4,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'tasktype': forms.Select(attrs={'class': 'form-control pointer','readonly':True}),
            'duration': forms.NumberInput(attrs={'class': 'form-control','readonly':True}),
            'taskdate': forms.TextInput(attrs={'class': 'form-control pointer','readonly':True}),
            'ifsubmitted': forms.Select(attrs={'class': 'form-control'}),
        }
    )

    formset = SbmitSheet(queryset=Sheet.objects.filter(~Q(ifsubmitted = '1'), empid= empid ,
    taskdate__gte=datetime.now()-timedelta(days=7), taskdate__lte=datetime.now()+ timedelta(days=7)
    ))
    EmpSheet = get_object_or_404(Employee, empid = empid)
    EmpData = Employee.objects.filter(empid = empid)
    dept = Department.objects.filter(deptcode = EmpSheet.deptcode)[:1]
    managid = 0
    # Get manager id for employee
    for data in dept:
        managid = data.managerid
    EmpID = 0
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    # empid = 123456
    if managid == EmpID:
        if request.method == 'POST':
            formset = SbmitSheet(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                # Get managers as hierarchicaly
                for obj in instances:
                    obj.submittedby = request.session['EmpID']
                    obj.submitteddate = datetime.now()
                    obj.save()
                return HttpResponseRedirect(reverse('ns-project:all-sheets'))
        else:
            formset = formset
    else:
        raise Http404
    # form = form_class(request.POST or None)
    return render(request, 'project/update_sheet.html', {'form': formset,'EmpData':EmpData})

def DetailseSheet(request,empid):
    EmpData = Employee.objects.filter(empid = empid)
    allsheet = Sheet.objects.filter(empid =empid)
    return render(request, 'project/details_sheets.html', {'EmpData':EmpData, 'allsheet':allsheet})

@login_required
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
@login_required
def AddSheet(request):
    AddSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate'), extra=7,
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
            managercode = manager_2 = manager_3 = manager_4 = 0
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
            messages.success(request, _("Post Submit"))
            return HttpResponseRedirect(reverse('ns-project:my-sheet'))
    else:
        formset = formset
    # form = form_class(request.POST or None)
    return render(request, 'project/add-sheet.html', {'form': formset})

def AddProject(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_obj= form.save(commit=False)
            try:
               status_obj= ProjectStatus.objects.get(isdefault=1)
            except :
               status_obj= ProjectStatus.objects.order_by('priority')[0]

            project_obj.status=status_obj
            project_obj.createdby=request.session.get('EmpID', '1056821208')
            project_obj.createddate= datetime.now()
            #save to database
            project_obj.save()
            # redirect to a new URL:
            messages.success(request, _("Project has created successfully"))
            return HttpResponseRedirect(reverse('ns-project:project-list'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project/add_project.html', {'form': form,'action_name': _('Ad Project')})

def ProjectList(request):
    createdBy=request.session.get('EmpID', '1056821208')
    project_list= Project.objects.all().filter(createdby__exact=createdBy).order_by('-id')
    paginator = Paginator(project_list, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)

    context = {'project_list':_plist}
    return render(request, 'project/projects.html', context)

def ProjectDetail(request,pk):
    project_detail= get_object_or_404(Project,pk=pk)
    createdBy=request.session.get('EmpID', '1056821208')
    project_list= Project.objects.all().filter(createdby__exact=createdBy).exclude(status=4).order_by('-id')

    context={'project_detail':project_detail,'project_list':project_list}
    return render(request, 'project/project_detail.html', context)

def ProjectEdit(request,pk):
    instance = get_object_or_404(Project,pk=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
       instance=form.save()
       instance.save()
       messages.success(request, _("Project has updated successfully"), fail_silently=True,)
       return HttpResponseRedirect(reverse('ns-project:project-list'))
    else:
        # Set the messages level back to default.
        #messages.add_message(request, messages.ERROR, 'Can not update project.', fail_silently=True, extra_tags='alert')
        #messages.error(request, _("Can not update project."))
        return render(request, 'project/add_project.html', {'form': form,'action_name': _('Edit Project')})

def ProjectDelete(request,pk):
    p= get_object_or_404(Project,pk=pk)
    emp_obj=Employee.objects.get(empid__exact=p.createdby)
    if request.method == 'POST':
          Project.objects.filter(id=p.id).delete()
          messages.success(request, _("Project has deleted successfully"), fail_silently=True,)
          return HttpResponseRedirect(reverse('ns-project:project-list'))
    else:
          context={'p':p,'emp_obj':emp_obj}
          return render(request, 'project/project_delete.html',context)

def ProjectTask(request,pk):
    createdBy=request.session.get('EmpID', '1056821208')
    task_list= Task.objects.all().filter(createdby__exact=createdBy, projectid__exact=pk).order_by('-id')
    paginator = Paginator(task_list, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)

    context = {'tasks':_plist}
    return render(request, 'project/tasks.html', context)
