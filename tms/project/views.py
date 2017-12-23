from django.shortcuts import render, render_to_response ,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect,Http404 ,HttpResponseForbidden
from .models import *
from .forms import *
from tms.ldap import *
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
from simple_history.utils import update_change_reason
from idlelib.debugobj import _object_browser
from .timesheet import *
from _datetime import date
from django.forms.models import modelformset_factory




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
    # Populate User From Ldap Without Login
    from django_auth_ldap.backend import LDAPBackend
    # ldapClient = ldap.initialize(AUTH_LDAP_SERVER_URI)
    # ldapClient.set_option(ldap.OPT_REFERRALS, 2000)
    # ldapClient.page_size = 10
    # ldapClient.bind(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
    # ldapClient.result()
    # results = ldapClient.search_s("OU=intranet,DC=stats,DC=gov,DC=sa",ldap.SCOPE_SUBTREE)
    # results.sizelimit = 1500
    # for result in results:
    #   result_dn = result[0]
    #   result_attrs = result[1]
    # ldap_backend = LDAPBackend()
    # ldap_backend.populate_user('aalbatil@stats.gov.sa')
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

@login_required
def ProjectList(request,project_status=None):
    EmpID = request.session.get('EmpID')
    emp_data  = get_object_or_404(Employee, empid = EmpID)
    dept_data = get_object_or_404(Department, deptcode = request.session.get('DeptCode'))

    tasks_list = Task.objects.filter(assignedto = EmpID)
    # Q(assignedto = EmpID)|
    # Q(departementid = request.session.get('DeptCode'))
    # )
    if EmpID == dept_data.managerid:
        tasks_list = Task.objects.filter(
        Q(assignedto = EmpID)|
        Q(departementid = request.session.get('DeptCode'))
        )
    all_project = Project.objects.all()

    project_id = []
    aDict = {}
    allTakProgress = 0
    projectProgress=0
    for data in tasks_list:
        project_id.append(data.projectid)

    project_list= Project.objects.all().filter(
    Q( createdby__exact=EmpID)|
    Q(id__in = project_id)
    ).order_by('-id')

    #check fi;ter by status
    if project_status =="all" :
          project_list=project_list
    elif project_status is not None :
         project_status = project_status.lower()
         project_list=project_list.filter(status__name__contains=project_status)

    for project in project_list:
        task_list = Task.objects.all().filter(projectid= project.id)
        allTakProgress = 0
        for data in task_list:
            if data.progress is not None:
                allTakProgress = allTakProgress + data.progress
            if len(task_list)==0:
                projectProgress=0
            else :
                projectProgress = round(allTakProgress/len(task_list), 2)
            aDict.update({project.id: projectProgress})

    paginator = Paginator(project_list, 20) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)

    context = {'project_list':_plist , 'aDict':aDict}
    return render(request, 'project/projects.html', context)

@login_required
def ProjectDetail(request,pk):
    project_detail= get_object_or_404(Project,pk=pk)
    EmpID=request.session.get('EmpID')
    tasks_list = Task.objects.filter(projectid__exact = pk)

    allTakProgress = 0
    projectProgress=0
    project_id = []
    for data in tasks_list:
        project_id.append(data.projectid)
        allTakProgress=allTakProgress+data.progress
    if len(tasks_list)==0:
        projectProgress=0
    else :
        projectProgress=round(allTakProgress/len(tasks_list), 2)

    project_list = Project.objects.all().filter(
    Q(createdby__exact=EmpID)|
    Q(id__in = project_id)
    ).exclude(status=4).order_by('-id')

    history=Task.history.filter(projectid=pk)[:10:1]
    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'project_detail':project_detail,'project_list':project_list,'current_url':current_url,'projectProgress':projectProgress,
    'taskprogress':allTakProgress,'tasks_list':tasks_list,'history':history}
    return render(request, 'project/project_detail.html', context)

@login_required
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
@login_required
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

@login_required
def ProjectTask(request,pk,task_status=None):
    current_url ="ns-project:" + resolve(request.path_info).url_name
    empid = request.session.get('EmpID')
    project_detail= get_object_or_404(Project,pk=pk)
    tasks_list = Task.objects.filter(assignedto = empid)
    project_id = []
    for data in tasks_list:
        project_id.append(data.projectid)

    project_list= Project.objects.all().filter(
    Q(createdby__exact=empid)|
    Q(id__in = project_id)
    ).exclude(status=4).order_by('-id')

    task_list= Task.objects.all().filter(
         Q(projectid__exact=pk)&
         Q(createdby__exact=empid)|
         Q(assignedto = empid,projectid__exact=pk)
         ).order_by('-id')

    if task_status=="all":
         task_list= task_list

    elif task_status=="unclosed":
         task_list = task_list.exclude(status__exact='Closed')
    elif task_status=="assignedtome":
         task_list= task_list.filter(assignedto__exact=empid)
    elif task_status=="new":
         task_list= task_list.filter(status__exact='New')
    elif task_status=="inprogress":
         task_list= task_list.filter(status__exact='InProgress')
    elif task_status=="finishedbyme":
         task_list= task_list.filter(finishedby__exact=empid,status__exact='Done')
    elif task_status=="done":
         task_list= task_list.filter(status__exact='Done')
    elif task_status=="closed":
         task_list= task_list.filter(status__exact='Closed')
    elif task_status=="cancelled":
         task_list= task_list.filter(status__exact='Cancelled')
    elif task_status=="hold":
         task_list= task_list.filter(status__exact='Hold')
    elif task_status=="delayed":
         task_list= task_list.filter(enddate__lt = datetime.today())
    elif task_status=="assignedtodept":
         task_list= task_list.filter(departementid__exact= request.session['DeptCode'])



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

    #relace empid with empname
#     for data in _plist:
#
#           try:
#                 data.assignedto=Employee.objects.get(empid=data.assignedto).empname
#           except :
#                 data.assignedto=data.assignedto
#           try:
#                 data.departementid=Department.objects.get(deptcode__exact = data.departementid).deptname
#           except :
#                data.departementid=data.departementid


    #task_list =data


    context = {'tasks':_plist,'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
    return render(request, 'project/tasks.html', context)


class ProjectMembersListView(ListView):

    model = ProjectMembers
    paginate_by=3
    def get_context_data(self, **kwargs):
        context = super(ProjectMembersListView, self).get_context_data(**kwargs)

        return context

@login_required
def ProjectTaskDetail(request,projectid,taskid):
    assignToEmp=None
    assignToDept=None

    createdBy=request.session['EmpID']
    project_list= Project.objects.all().filter(createdby__exact=createdBy).exclude(status=4).order_by('-id')
    current_url ="ns-project:project-task"
    project_detail= get_object_or_404(Project,pk=projectid)
    task_detail= get_object_or_404(Task,projectid__exact= projectid,pk=taskid)
    projectmembers= ProjectMembers.objects.all().order_by('-id')
    createdby=get_object_or_404(Employee,empid__exact=task_detail.createdby);
    try:
        assignToEmp=Employee.objects.get(empid__exact=task_detail.assignedto);
    except:
        assignToEmp=None

    try:
       assignToDept=Department.objects.get(deptcode__exact=task_detail.departementid);
    except:
       assignToDept = None

    try:
        finishedby=Employee.objects.get(empid__exact=task_detail.finishedby);
    except:
        finishedby = None
    try:
        cancelledby=Employee.objects.get(empid__exact=task_detail.cancelledby);
    except:
        cancelledby = None
    try:
        closedby=Employee.objects.get(empid__exact=task_detail.closedby);
    except:
        closedby = None

    history=Task.history.filter(id=taskid)[:10:1]
    context = {'project_detail':project_detail,
               'project_list':project_list,
               'current_url':current_url,
               'task':task_detail,
               'projectmembers':projectmembers,
               'assignToEmp':assignToEmp,'assignToDept':assignToDept,
               'createdby':createdby,
               'finishedby':finishedby,
               'cancelledby':cancelledby,
               'closedby':closedby,
               'history':history,
               }
    return render(request, 'project/project_task_detail.html', context)

@login_required
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
            #add to history
            update_change_reason(_obj, _("Update start date for task by ")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['notes'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('InProgress')
            data['icon'] = "p_%s" %pk
            data['message'] = _('Start Date Updated successfully for Task number %s ' %pk)
            data['html_form'] = render_to_string('project/task/update_start_task.html',request=request)
            return JsonResponse(data)

    # if a GET (or any other method) we'll create a blank form
    else:
        data['form_is_valid'] = False
    context = {'form': TaskStartForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_start_task.html',context,request=request,)
    return JsonResponse(data)

@login_required
def updateTaskFinish(request,pk):
    data = dict()
    errors = []

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskFinishForm(request.POST)
        if form.is_valid():
            _obj.ftime=form.cleaned_data['ftime']
            _obj.status="Done"
            _obj.progress=100
            _obj.finisheddate=datetime.now()
            _obj.finishedby=request.session.get('EmpID', '1056821208')
            _obj.lasteditdate=datetime.now()
            _obj.lasteditby=request.session.get('EmpID', '1056821208')
            _obj.save()
             #add to history
            update_change_reason(_obj, _("Finish Task ")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['notes'])
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
    return JsonResponse(data)

@login_required
def updateTaskClose(request,pk):
    data = dict()
    errors = []

    if 'reason' in request.POST:
        reason = request.POST['reason']
        if not reason:
            errors.append(_('Enter a reason .'))

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskCloseForm(request.POST )
        if form.is_valid():
            _obj.status="Closed"
            _obj.closeddate=datetime.now()
            _obj.closedby= request.session.get('EmpID', '1056821208')
            _obj.closeddate=datetime.now()
            _obj.lasteditdate=datetime.now()
            _obj.save()
               #add to history
            update_change_reason(_obj, _("Close Task by ")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['reason'])
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

@login_required
def updateTaskCancel(request,pk):
    data = dict()
    errors = []
    if 'reason' in request.POST:
        reason = request.POST['reason']
        if not reason:
            errors.append(_('Enter a reason .'))

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskCancelForm(request.POST )
        if form.is_valid():
            _obj.status="Cancelled"
            _obj.cancelledby= request.session.get('EmpID', '1056821208')
            _obj.canceleddate=datetime.now()
            _obj.lasteditdate=datetime.now()
            _obj.save()
               #add to history
            update_change_reason(_obj, _("Cancel Task by ")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['reason'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Cancelled')
            data['icon'] = "c_%s" %pk
            data['message'] = _('Task has been cancelled successfully for Task number #')+ pk
            data['html_form'] = render_to_string('project/task/update_cancel_task.html',request=request)
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False

    # if a GET (or any other method) we'll create a blank form
    context = {'form': TaskCancelForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_cancel_task.html',context,request=request)
    return JsonResponse(data)

@login_required
def updateTaskPause(request,pk):
    data = dict()
    errors = []
    if 'note' in request.POST:
        note = request.POST['note']
        if not note:
            errors.append(_('Enter a note .'))

    _obj =  get_object_or_404(Task,pk=pk)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskPauseForm(request.POST )
        if form.is_valid():
            _obj.status="Hold"
            _obj.lasteditdate=datetime.now()
            _obj.save()
            #add to history
            update_change_reason(_obj, _("Task Pause by ")+ request.session['EmpName'] +",<i class=\"fa fa-comment\"></i>" + form.cleaned_data['note'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Hold')
            data['icon'] = "c_%s" %pk
            data['message'] = _('Task has been continuous successfully for Task number #')+ pk
            data['html_form'] = render_to_string('project/task/update_pause_task.html',request=request)
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False

    # if a GET (or any other method) we'll create a blank form
    context = {'form': TaskPauseForm(),'pk':pk,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_pause_task.html',context,request=request)
    return JsonResponse(data)

@login_required
def ganttChart(request,pk):

    context={}
    return render(request, 'project/project_ganttchart.html', context)

@login_required
def projectFlowUp(request):
     task_list=''
     if request.method == 'GET':
        # form.fields["department"].queryset = Employee.objects.filter(deptcode = dept)
        form = FollowupForm(request.GET)
        dept = request.GET.get('departement')
        employee = request.GET.get('employee')
        status = request.GET.get('taskstatus')
        if dept:
            task_list=VFollowup.objects.filter(deptcode__exact=dept)
            form.fields["employee"].queryset = Employee.objects.filter(deptcode = dept)
        if status and dept:
            task_list=task_list.filter(status__exact=status)
        if employee and dept:
            task_list=task_list.filter(assignedto__exact=employee)

        if task_list:
            task_list=task_list.order_by('-id')

        res=len(task_list)
        paginator = Paginator(task_list, 5) # Show 5 contacts per page

        page = request.GET.get('page')
        try:
            task_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            task_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            task_list = paginator.page(paginator.num_pages)


     context={'form':form,'tasks':task_list,'res':res}
     return render(request, 'project/project_followup.html', context)

@login_required
def ProjectTeam(request,project_id):
    project_detail= get_object_or_404(Project,pk=project_id)
    EmpID=request.session.get('EmpID')
    tasks_list = Task.objects.filter(assignedto = EmpID)
    projectid = []
    for data in tasks_list:
        projectid.append(data.projectid)
    project_list= Project.objects.all().filter(
    Q(createdby__exact=EmpID)|
    Q(id__in = projectid)
    ).exclude(status=4).order_by('-id')
    all_emp = VStatisticstaskdata.objects.filter(projectid = project_id)
    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'all_emp':all_emp,'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
    return render(request, 'project/project_team.html', context)

@login_required
def AddTask(request,project_id):
    empdata = get_object_or_404(Employee,empid=request.session.get('EmpID'))
    deptcode = request.session.get('DeptCode')
    # upload_file = UploadFile
    upload = modelformset_factory(Media,form=UploadFile,extra = 1)
    FormSet = upload(queryset=Media.objects.filter(taskid = 0))
    form = AddTaskForm()
    # form.assignedto.queryset = Employee.objects.filter(deptcode = deptcode)
    form.fields["employee"].queryset = Employee.objects.filter(deptcode = deptcode)
    if request.method=='POST':
        assignto_employee = request.POST.get('employee', False)
        assignto_department = request.POST.get('department', False)
        form = AddTaskForm(request.POST)
        if form.is_valid():
            # form.save()
            project_obj = form.save(commit=False)
            project_obj.projectid = project_id
            project_obj.status = 'New'
            project_obj.createdby = request.session.get('EmpID')
            project_obj.lasteditdate = datetime.now()
            project_obj.createddate = datetime.now()
            project_obj.progress = 0
            if assignto_employee:
                project_obj.assignedto = assignto_employee
                project_obj.assigneddate = datetime.now()
            if assignto_department:
                project_obj.departementid = assignto_department
                project_obj.assigneddate = datetime.now()
            project_obj.save()
            upload_form = upload(request.POST, request.FILES)
            if upload_form.is_valid():
                obj_file = upload_form.save(commit=False)
                for obj in obj_file:
                    obj.projectid = project_id
                    obj.taskid = project_obj.id
                    obj.save()
            else:
                data = {'is_valid': False}
                return JsonResponse(data)
            if assignto_employee:
                assigntodata = get_object_or_404(Employee , empid = assignto_employee )
                update_change_reason(project_obj, _("Add new Task By") + empdata.empname + " " + _("And Assign to") + " " + assigntodata.empname)
            elif assignto_department:
                assigntodata = get_object_or_404(Department , deptcode = assignto_department )
                update_change_reason(project_obj, _("Add new Task By") + empdata.empname + " " +_("And Assign to") + " " + assigntodata.deptname)
            else:
                update_change_reason(project_obj, _("Add new Task By")+empdata.empname)

            messages.success(request, _("Task Added"))
            return HttpResponseRedirect(reverse('ns-project:project-task' , kwargs={'pk':project_id} ))

            # project_obj.save()
    else:
        form = form

    context ={'upload_file':FormSet, 'form':form}
    return render (request,'project/add_task.html', context)

@login_required
def ProjectTaskDelete(request,projectid,taskid):
    try:
        task= get_object_or_404(Task,createdby__exact= request.session['EmpID'],projectid__exact= projectid,pk=taskid)
        project=get_object_or_404(Project,pk=projectid)
        employee=get_object_or_404(Employee,empid__exact= task.createdby)
    except:
        task=None
        project=None
    if request.method == 'POST':
              Task.objects.filter(id=task.id).delete()
              messages.success(request, _("Task has been deleted successfully"), fail_silently=True,)
              return HttpResponseRedirect(reverse('ns-project:project-task', kwargs={'pk':project.id} ))
    else:
          context={'task':task,'project':project,'employee':employee}
          return render(request, 'project/project_task_delete.html', context)

@login_required
def updateTaskAssignto(request,pk,save=None):
    data = dict()
    errors = []
    assigntype="emp"
    employee=None
    departement=None
    _assign=""
    _obj =  get_object_or_404(Task,pk=pk)


    if request.method == 'POST':
        form = TaskAssignToForm(request.POST )
        form.fields["employee"].queryset = Employee.objects.filter(deptcode = request.session['DeptCode'])
        if 'assigntype' in request.POST:
            assigntype = request.POST['assigntype']
        if not assigntype:
            errors.append(_('Enter select assigntype'))
        if assigntype=="emp" :
             employee=request.POST.get('employee')
             data['assignedto_empid']=employee
             form.fields["departement"].required=False  #make required filed in model false
#              if not employee:
#                  errors.append(_('Enter a employee .'))
        if assigntype=="dept" :
             departement=request.POST.get('departement')
             data['assignedto_depid']=departement
             form.fields["employee"].required=False  #make required filed in model false


        if form.is_valid():
            if save !="False" :
             
                if  employee :
                    _obj.assignedto=int(form.cleaned_data['employee'].empid)
                    _assign=form.cleaned_data['employee'].empname
                    _obj.departementid=Employee.objects.get(empid__exact= _obj.assignedto).deptcode

                    
                elif departement :
                        _obj.departementid=int(form.cleaned_data['departement'].deptcode)
                        _assign=form.cleaned_data['departement'].deptname
                        _obj.assignedto=None

                      
            _obj.canncelleddate=None
            _obj.cancelledby=None
            _obj.closeddate=None
            _obj.closedby=None  
            _obj.finisheddate=None
            _obj.finishedby=None   
            _obj.lasteditdate=datetime.now()
            _obj.save()
            #add to history
            update_change_reason(_obj,_(" by ")+ request.session['EmpName']  +  _(" ,  Assign Task to ")+  str(_assign))
            messages.success(request, "<i class=\"fa fa-check\" aria-hidden=\"true\"></i>"+_(" Task has been updated successfully "), fail_silently=True,)

            data['form_is_valid'] = True
            data['id'] = pk
            data['message'] = "<i class=\"fa fa-check\" aria-hidden=\"true\"></i>" + _('Task has been assigned successfully for Task number #')+ pk
            data['html_form'] = render_to_string('project/task/update_assignto_task.html',request=request)
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['errors'] = errors.append(form.errors)

    form = TaskAssignToForm()
      #if user not create dtha task disable assifn to departement
    if _obj.createdby!= request.session['EmpID']:
        form.fields["departement"].disabled = True
    if assigntype=="emp" :
        form.fields["departement"].disabled = True
    if assigntype=="dept" :
        form.fields["employee"].disabled = True
    form.fields["assigntype"].initial = assigntype
    form.fields["employee"].queryset = Employee.objects.filter(deptcode = request.session['DeptCode'])
    context = {'form': form,'pk':pk,'save':save,'errors':errors}
    data['html_form'] = render_to_string('project/task/update_assignto_task.html',context,request=request)
    return JsonResponse(data)

@login_required
def updateTaskProgress(request,pk):
    data = dict()
    _task =  get_object_or_404(Task,pk=pk)
    # create a form instance and populate it with data from the request:
    form = TaskProgressForm(request.POST or None, instance=_task)
    if form.is_valid():
        _task.progress= form.cleaned_data['progress']
#             if _task.progress==100 :
#                 _task.status="Done"
        _task.lasteditdate=datetime.now()
        _task.save()
           #add to history
        update_change_reason(_task, _("Task Progress chenged by ")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['note'])
        data['form_is_valid'] = True
        data['message'] = _('Progress Updated successfully for Task number'+ pk)
        data['html_form'] = render_to_string('project/task/update_progress_task.html',request=request)
        return JsonResponse(data)
    else:
        data['form_is_valid'] = False

    # if a GET (or any other method) we'll create a blank form
    context = {'form': form,'pk':pk}
    data['html_form'] = render_to_string('project/task/update_progress_task.html',context,request=request)
    return JsonResponse(data)

@login_required
def ProjectTaskEdit(request,projectid,taskid):
    employee=get_object_or_404(Employee,empid__exact=request.session['EmpID']);
    project_list= Project.objects.all().filter(createdby__exact=employee).exclude(status=4).order_by('-id')
    current_url ="ns-project:project-task"
    project_detail= get_object_or_404(Project,pk=projectid)
    task_detail= get_object_or_404(Task,pk=taskid)
    form = EditTaskForm(request.POST or None, instance=task_detail)
    # for use in futrure
    #form.fields["createdby"].queryset = Employee.objects.filter(deptcode = request.session['DeptCode'])
    #form.fields["createdby"].initial=task_detail.createdby

    try:
        assignTo=Employee.objects.get(empid__exact=task_detail.assignedto);
    except:
        assignTo = None
    try:
        finishedby=Employee.objects.get(empid__exact=task_detail.finishedby);
    except:
        finishedby = None
    try:
        cancelledby=Employee.objects.get(empid__exact=task_detail.cancelledby);
    except:
        cancelledby = None
    try:
        closedby=Employee.objects.get(empid__exact=task_detail.closedby);
    except:
        closedby = None

    if form.is_valid():
        instance=form.save()
        instance.status=form.cleaned_data['status']
        #instance.finisheddate=form.cleaned_data['finisheddate']
        #check if status changed to new
        if form.cleaned_data['status'] =="New" or form.cleaned_data['status'] =="Inprogress" :
           instance.closedby=None
           instance.closeddate=None
           instance.canceleddate=None
           instance.cancelledby=None
           instance.finisheddate=None
           instance.finishedby=None
        if form.cleaned_data['status']=="Done":
           instance.closedby=None
           instance.closeddate=None
           instance.canceleddate=None
           instance.cancelledby=None
           instance.finishedby=request.session['EmpID']
        if form.cleaned_data['status']=="Hold":
           pass
        if form.cleaned_data['status']=="Cancelled":
            instance.canceleddate=datetime.now()
            instance.cancelledby=request.session['EmpID']
        if form.cleaned_data['status']=="Closed":
            instance.closeddate=datetime.now()
            instance.closeby=request.session['EmpID']

        instance.lasteditdate=datetime.now()
        instance.lasteditby=request.session['EmpID']


        instance.save()
        messages.success(request, _(" Task has been updated successfully "), fail_silently=True,)
        #add to history
        update_change_reason(instance, _(" Edit Task successfully by ")+  str( employee.empname)+ (",    <i class=\"fa fa-comment\"></i>  "+ form.cleaned_data['note']  if form.cleaned_data['note'] else " "))
        return HttpResponseRedirect(reverse('ns-project:project-task-detail', kwargs={'projectid':projectid,'taskid':taskid}))
    else:
        context = {'project_detail':project_detail,
               'project_list':project_list,
               'current_url':current_url,
               'task':task_detail,
               'form':form,
                'assignTo':assignTo,
                'createdby':employee,
                'finishedby':finishedby,
                'cancelledby':cancelledby,
                'closedby':closedby,
               }
        return render(request, 'project/project_task_edit.html', context)

@login_required
def TaskListExternal(request,task_status=None):   
    current_url ="ns-project:" + resolve(request.path_info).url_name
    empid = request.session.get('EmpID')
    tasks_list = Task.objects.filter(assignedto = empid)
     
    
    project_id = []
    for data in tasks_list:
        project_id.append(data.projectid)


    #no of new task 
    new_tasks_count= len(Task.objects.all().filter(Q(status__exact='New')&(
         Q(assignedto = empid)|Q(departementid =  request.session['DeptCode']))
         ).exclude(createdby__exact=empid))


    #get all tasks assign to dept from external project 
    task_list= Task.objects.all().filter(
         Q(departementid =  request.session['DeptCode'])
         ).exclude(createdby__exact=empid).order_by('-id')

 
    if task_status=="all":
         task_list= task_list

    elif task_status=="unclosed":
         task_list = task_list.exclude(status__exact='Closed')
    elif task_status=="assignedtome":
         task_list= task_list.filter(assignedto__exact=empid)
    elif task_status=="new":
         task_list= task_list.filter(status__exact='New')
    elif task_status=="inprogress":
         task_list= task_list.filter(status__exact='InProgress')
    elif task_status=="finishedbyme":
         task_list= task_list.filter(finishedby__exact=empid,status__exact='Done')
    elif task_status=="done":
         task_list= task_list.filter(status__exact='Done')
    elif task_status=="closed":
         task_list= task_list.filter(status__exact='Closed')
    elif task_status=="cancelled":
         task_list= task_list.filter(status__exact='Cancelled')
    elif task_status=="hold":
         task_list= task_list.filter(status__exact='Hold')
    elif task_status=="delayed":
         task_list= task_list.filter(enddate__lt = datetime.today())
    elif task_status=="assignedtodept":
         task_list= task_list.filter(departementid__exact= request.session['DeptCode'])


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


    context = {'tasks':_plist,'current_url':current_url,'new_tasks_count':new_tasks_count}
    return render(request, 'project/tasks_from_external_dept.html', context)