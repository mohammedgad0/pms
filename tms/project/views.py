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
from django.views.generic import UpdateView, ListView
from .filters import SheetFilter
from django.template.loader import  render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.urlresolvers import resolve


class BaseSheetFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        taskdesc = []
        for form in self.forms:
            taskdescs = form.cleaned_data['taskdescs']
            if taskdescs in titles:
                raise forms.ValidationError("Articles in a set must have distinct titles.")
            titles.append(title)

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

#@login_required
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
    from django_auth_ldap.backend import LDAPBackend
    ldap_backend = LDAPBackend()
    ldap_backend.populate_user('aalbatil@stats.gov.sa')
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
@permission_required('project.add_sheet',raise_exception=True)
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
def EmpSheet(request,empid):
    '''
    Page For Manager to See Employees Sheets
    '''
    EmpData = get_object_or_404(Employee, empid = empid)
    deptcode = EmpData.deptcode
    alldept = request.session.get('TreeDept', '0')
    # referer = 'test'
    # URL = request.META.get('HTTP_REFERER')
    # if URL:
    #     referer= URL.split("/")[-2]
    # request.session['CanView'] = False
    # if referer == 'dept':
    #     request.session['CanView'] = True
    his_manager = False
    if str(EmpData.managercode) == str(request.session['EmpID']):
        his_manager = True
    if str(EmpData.managercode) == str(request.session['EmpID']) or deptcode in alldept:
        sheet_list = Sheet.objects.filter(empid = empid)
        start = request.GET.get("q_start")
        end = request.GET.get("q_end")
        if start:
            sheet_list = Sheet.objects.filter(empid = empid,taskdate__gte=start, taskdate__lte=end)
        # EmpData = Employee.objects.filter(empid = empid)
        sheet_filter = SheetFilter(request.GET, queryset=sheet_list)
    else:
        raise Http404

    return render(request, 'project/emp_sheet.html', {'filter': sheet_filter,'EmpData':EmpData,"his_manager":his_manager})

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

def AllDept(request):
    '''
    All departments as tree based on user logged in
    '''
    DeptCode = request.session['DeptCode']
    dept_level_1 = ApfDeptView.objects.filter(resp_dept_code = DeptCode)
    dept_level_2 = []
    dept_level_3 = []
    dept_level_4 = []
    for dept in dept_level_1:
        dept2 = dept.dept_code
        # name = dept.dept_name
        dept_level_2.append(dept2)
        # dept_level_2.append(name)
        dept = ApfDeptView.objects.filter(resp_dept_code = dept2)
        for data in dept:
            dept3= data.dept_code
            # name = data.dept_name
            dept_level_3.append(dept3)
            # dept_level_3.append(name)
            dept = ApfDeptView.objects.filter(resp_dept_code = dept3)
            for data in dept:
                dept4 = data.dept_code
                dept_level_4.append(dept4)
    all_dept =  dept_level_2 + dept_level_3 + dept_level_4
    all_dept.append(DeptCode)
    request.session['TreeDept'] = all_dept
    le = len(list(all_dept))
    SelectDept = VDeptsheetsdata.objects.filter(deptcode__in = all_dept)
    AllDept = VDeptsheetsdata.objects.filter(deptcode__in = all_dept)
    query = request.GET.get("q")
    if query and query != '0':
        AllDept = VDeptsheetsdata.objects.filter(
        Q(deptcode = query)
        )
    # for data in AllEmp:
    count = len(list(AllDept))
    if count == 0:
        messages.info(request, _("No data there"))
        context = {'alldept':AllDept,"count":count,"selectdept":SelectDept}
        return render(request, 'project/sheet_all_dept.html',context)
    context = {'alldept':AllDept,"count":count,"selectdept":SelectDept,"deptcode":DeptCode,'dept2':dept_level_1
    ,'level3':dept_level_3,'level4':dept_level_4,'alldepartment':all_dept,'len':le
    }

    return render(request, 'project/sheet_all_dept.html',context)

@login_required
def UpdateSheet(request,empid):
    SbmitSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate','ifsubmitted'), extra=0,
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

    start = request.GET.get("q_start")
    end = request.GET.get("q_end")
    if start:
        formset = SbmitSheet(queryset=Sheet.objects.filter(~Q(ifsubmitted = '1'), empid= empid ,
        taskdate__gte=start, taskdate__lte=end
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
                    if obj.ifsubmitted == '1':
                        obj.status = '1'
                    if obj.ifsubmitted == '2':
                        obj.status = '3'
                    obj.save()
                return HttpResponseRedirect(reverse('ns-project:all-sheets'))
        else:
            formset = formset
    else:
        raise Http404
    # form = form_class(request.POST or None)
    return render(request, 'project/update_sheet.html', {'form': formset,'EmpData':EmpData})

@login_required
def DetailseSheet(request,empid):
    EmpData = Employee.objects.filter(empid = empid)
    allsheet = Sheet.objects.filter(empid =empid)
    return render(request, 'project/details_sheets.html', {'EmpData':EmpData, 'allsheet':allsheet})

@login_required
def DeptSheet(request,deptcode):
    if request.user.is_authenticated():
        # DeptCode = request.session['DeptCode']
        EmpID = request.session['EmpID']
    dept = Department.objects.filter(deptcode= deptcode)[:1]
    managid = '0'
    sheets = None
    # referer = ' '
    # URL = request.META.get('HTTP_REFERER')
    # if URL:
    #     referer= URL.split("/")[-2]
    # request.session['CanView'] = False
    # if referer == 'all_dept_sheet':
    #     request.session['CanView'] = True
    alldept = request.session.get('TreeDept', '0')
    for data in dept:
        managid = data.managerid
    if managid == EmpID or deptcode in alldept:
        # if this user is manager
        AllEmp = "0"
        #count all data
        emp_count = Employee.objects.filter(deptcode = deptcode).count()
        total_task = Sheet.objects.filter(deptcode = deptcode).count()
        submitted_task = Sheet.objects.filter(deptcode = deptcode, status = 2).count()
        not_submitted_task = Sheet.objects.filter(deptcode = deptcode, status = 3).count()
        AllEmp = VSheetsdata.objects.filter(deptcode = deptcode).order_by('new')
        query = request.GET.get("q")
        if query:
            AllEmp = VSheetsdata.objects.filter(
            Q(deptcode = deptcode)&
            Q(employeename__icontains = query)
            )
    else:
        raise Http404
    count = len(list(AllEmp))
    if count == 0:
        messages.info(request, _("No data"))
        return render(request, 'project/all_sheets.html')
    context = {'allemp':AllEmp,"count":count,"total_task":total_task,
    "submitted_task":submitted_task,"n_task":not_submitted_task,"emp_count":emp_count}


    return render(request, 'project/all_sheets.html',context)

# Add sheet form
@login_required
def AddSheet(request):
    AddSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate'),can_delete=True, extra=7,
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
    )
    )
    # formset = AddSheet(initial=[{'tasktype': 'm'}])

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
                obj.status = '0'
                if obj.createddate:
                    obj.editedate = datetime.now()
                else:
                    obj.createddate = datetime.now()
                obj.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, _("Post Submit"))
            return HttpResponseRedirect(reverse('ns-project:my-sheet'))
    else:
        formset = formset
    # form = form_class(request.POST or None)
    return render(request, 'project/add-sheet.html', {'form': formset})

@login_required
def SubmitSheet(request,pk):
    '''
    Submit or not submit individual sheet by manager.
    '''
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    SbmitSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate','ifsubmitted'), can_delete=True, extra=0,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'tasktype': forms.Select(attrs={'class': 'form-control pointer','readonly':True}),
            'duration': forms.NumberInput(attrs={'class': 'form-control','readonly':True}),
            'taskdate': forms.TextInput(attrs={'class': 'form-control pointer','readonly':True}),
            'ifsubmitted': forms.Select(attrs={'class': 'form-control'}),
        }
    )
    formset = SbmitSheet(queryset=Sheet.objects.filter(id = pk,ifsubmitted='0' ))
    # taskdate__gte=datetime.now()-timedelta(days=7), taskdate__lte=datetime.now()+ timedelta(days=7)
    SheetData = get_object_or_404(Sheet,pk=pk)
    sheetid = SheetData.empid
    employeeid = SheetData.empid
    # if EmpID == str(sheetid):
    if request.method == 'POST':
        formset = SbmitSheet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in instances:
                obj.submittedby = request.session['EmpID']
                obj.submitteddate = datetime.now()
                if obj.ifsubmitted == '1':
                    obj.status = '1'
                if obj.ifsubmitted == '2':
                    obj.status = '3'
                obj.save()
            messages.success(request, _("Post Done"))
            return HttpResponseRedirect(reverse('ns-project:emp-sheet', kwargs={'empid':employeeid} ))
    else:
        formset = formset
    # else:
    #     raise Http404
    # form = form_class(request.POST or None)
    return render(request, 'project/submit_sheet.html', {'form': formset,'Sheetid':sheetid,'EmpID':EmpID})

@login_required
def EditSheet(request,pk):
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    SbmitSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate','ifsubmitted'), can_delete=True, extra=0,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control'}),
            'tasktype': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'taskdate': forms.TextInput(attrs={'class': 'form-control'}),
            'ifsubmitted': forms.Select(attrs={'class': 'form-control'}),
        }
    )
    formset = SbmitSheet(queryset=Sheet.objects.filter(id = pk,ifsubmitted='0' ))
    # taskdate__gte=datetime.now()-timedelta(days=7), taskdate__lte=datetime.now()+ timedelta(days=7)
    SheetData = get_object_or_404(Sheet,pk=pk)
    sheetid = SheetData.empid
    if EmpID == str(sheetid):
        if request.method == 'POST':
            formset = SbmitSheet(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                # Get managers as hierarchicaly
                for obj in instances:
                    obj.editdate = datetime.now()
                    obj.ifsubmitted = 0
                    obj.save()
                for obj in formset.deleted_objects:
                    obj.delete()
                messages.success(request, _("Edit complete"))
                return HttpResponseRedirect(reverse('ns-project:my-sheet'))
        else:
            formset = formset
    else:
        raise Http404
    # form = form_class(request.POST or None)
    return render(request, 'project/edit_s_sheet.html', {'form': formset,'Sheetid':sheetid,'EmpID':EmpID})

@login_required
def ChangeStatus(request,pk):
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    ChangeStatus = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration','taskdate','reason','status'),extra=0,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'tasktype': forms.Select(attrs={'class': 'form-control pointer','readonly':True}),
            'duration': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'taskdate': forms.TextInput(attrs={'class': 'form-control pointer','readonly':True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
        }
    )
    formset = ChangeStatus(queryset=Sheet.objects.filter(ifsubmitted = '1',id = pk ))
    # taskdate__gte=datetime.now()-timedelta(days=7), taskdate__lte=datetime.now()+ timedelta(days=7)
    SheetData = get_object_or_404(Sheet,pk=pk)
    sheetid = SheetData.empid
    if EmpID == str(sheetid):
        if request.method == 'POST':
            formset = ChangeStatus(request.POST)
            if formset.is_valid():
                instances = formset.save(commit=False)
                # Get managers as hierarchicaly
                for obj in instances:
                    obj.statusdate = datetime.now()
                    obj.save()

                messages.success(request, _("Change status done"))
                return HttpResponseRedirect(reverse('ns-project:my-sheet'))
        else:
            formset = formset
    else:
        raise Http404
    # form = form_class(request.POST or None)
    return render(request, 'project/change_s_sheet.html', {'form': formset})


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
    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
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


def ProjectTask(request,pk,task_status=None):
    current_url ="ns-project:" + resolve(request.path_info).url_name
    empid=request.session.get('EmpID', '1056821208')
    project_detail= get_object_or_404(Project,pk=pk)
    project_list= Project.objects.all().filter(createdby__exact=empid).exclude(status=4).order_by('-id')

    if task_status=="all":
         task_list= Task.objects.all().filter(createdby__exact=empid, projectid__exact=pk).order_by('-id')
    elif task_status=="unclosed":
         task_list= Task.objects.all().filter(createdby__exact=empid, projectid__exact=pk).exclude(status__exact='Closed').order_by('-id')
    elif task_status=="assignedtome":
         task_list= Task.objects.all().filter( projectid__exact=pk,assignedto__exact=empid).order_by('-id')
    elif task_status=="new":
         task_list= Task.objects.all().filter(createdby__exact=empid, projectid__exact=pk,status__exact='New').order_by('-id')
    elif task_status=="inprogress":
         task_list= Task.objects.all().filter(createdby__exact=empid, projectid__exact=pk,status__exact='InProgress').order_by('-id')
    elif task_status=="finishedbyme":
         task_list= Task.objects.all().filter(finishedby__exact=empid, projectid__exact=pk,status__exact='Done').order_by('-id')
    elif task_status=="done":
         task_list= Task.objects.all().filter( projectid__exact=pk,status__exact='Done').order_by('-id')
    elif task_status=="closed":
         task_list= Task.objects.all().filter( projectid__exact=pk,status__exact='Closed').order_by('-id')
    elif task_status=="cancelled":
         task_list= Task.objects.all().filter( projectid__exact=pk,status__exact='Cancelled').order_by('-id')
    elif task_status=="hold":
         task_list= Task.objects.all().filter( projectid__exact=pk,status__exact='Hold').order_by('-id')
    elif task_status=="delayed":
         task_list= Task.objects.all().filter( projectid__exact=pk,enddate__lt = datetime.today()).order_by('-id')
    else :
       task_list= Task.objects.all().filter(createdby__exact=empid, projectid__exact=pk).order_by('-id')


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

    context = {'tasks':_plist,'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
    return render(request, 'project/tasks.html', context)

def ProjectTeam(request,pk):
    createdBy=request.session.get('EmpID', '1056821208')
    project_list= Project.objects.all().filter(createdby__exact=createdBy).exclude(status=4).order_by('-id')
    current_url ="ns-project:" + resolve(request.path_info).url_name
    project_detail= get_object_or_404(Project,pk=pk)
    projectmembers= ProjectMembers.objects.all().order_by('-id')

    paginator = Paginator(projectmembers, 5) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        _mlist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _mlist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _mlist = paginator.page(paginator.num_pages)


    #project team
    form=TeamForm()

    context = {'form':form,'project_detail':project_detail,'project_list':project_list,'current_url':current_url,'projectmembers':_mlist}
    return render(request, 'project/project_team.html', context)

class ProjectMembersListView(ListView):

    model = ProjectMembers
    paginate_by=3
    def get_context_data(self, **kwargs):
        context = super(ProjectMembersListView, self).get_context_data(**kwargs)

        return context


def ProjectTaskDetail(request,pk):
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


def updateStartDate(request,pk):
    data = dict()
    errors = []

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskStartForm(request.POST)
        if form.is_valid():
            _obj.realstartdate=form.cleaned_data['rsd']
            _obj.realstartby=request.session.get('EmpID', '1056821208')
            _obj.status="InProgress"
            _obj.lasteditdate=datetime.now()
            _obj.lasteditby=request.session.get('EmpID', '1056821208')
            _obj.save()
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('InProgress')
            data['icon'] = "p_%s" %pk
            data['message'] = _('Start Date Updated successfully for Task number %s ' %pk)
            data['html_form'] = render_to_string('project/update_start_task.html',request=request)
            return JsonResponse(data)

    # if a GET (or any other method) we'll create a blank form
    else:
        data['form_is_valid'] = False
    context = {'form': TaskStartForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/update_start_task.html',context,request=request,)
    return JsonResponse(data)


def updateTaskFinish(request,pk):
    data = dict()
    errors = []

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskFinishForm(request.POST)
        if form.is_valid():
            _obj.ftime=form.cleaned_data['ftime']
            _obj.status="Finished"
            _obj.finisheddate=datetime.now()
            _obj.finishedby=request.session.get('EmpID', '1056821208')
            _obj.lasteditdate=datetime.now()
            _obj.lasteditby=request.session.get('EmpID', '1056821208')
            _obj.save()
            data['form_is_valid'] = True
            data['icon'] = "f_%s" %pk
            data['id'] = pk
            data['status'] = _('Finished')
            data['message'] = _(' Finish Date Updated successfully for Task number %s ' %pk)
            data['html_form'] = render_to_string('project/task/update_finish_task.html',request=request)
            return JsonResponse(data)

    # if a GET (or any other method) we'll create a blank form
    else:
        data['form_is_valid'] = False
    context = {'form': TaskFinishForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_finish_task.html',context,request=request)
    return JsonResponse({data})


def updateTaskClose(request,pk):
    data = dict()
    errors = []

    if 'notes' in request.POST:
        notes = request.POST['notes']
        if not notes:
            errors.append(_('Enter a notes .'))

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskCloseForm(request.POST )
        if form.is_valid():
            _obj.closeddate=form.cleaned_data['ctime']
            _obj.status="Closed"
            _obj.closedby= request.session.get('EmpID', '1056821208')
            _obj.closeddate=datetime.now()
            _obj.lasteditdate=datetime.now()
            _obj.save()
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Closed')
            data['icon'] = "c_%s" %pk
            data['message'] = _(' Close Date Updated successfully for Task number %s ' %pk)
            data['html_form'] = render_to_string('project/task/update_close_task.html',request=request)
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False

    # if a GET (or any other method) we'll create a blank form
    context = {'form': TaskCloseForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_close_task.html',context,request=request)
    return JsonResponse(data)

def ganttChart(request,pk):

    context={}
    return render(request, 'project/project_ganttchart.html', context)

def projectFlowUp(request,pk):
    pass
    
