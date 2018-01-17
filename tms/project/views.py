from django.shortcuts import render, render_to_response ,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse ,HttpResponseRedirect,Http404 ,HttpResponseForbidden
from .models import *
from .forms import *
from tms.ldap import *
# from django.contrib.auth import login
from django.contrib.auth.views import *
from django.utils.translation import ugettext as _
from django.forms import formset_factory
from django.forms import BaseModelFormSet
from datetime import datetime , timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q , Count ,Avg
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User,Group
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
from django.forms.models import modelformset_factory
from unittest.case import expectedFailure
from django.core.mail import send_mail
from django.template.context_processors import request


def loginfromdrupal(request, email,signature,time):
    from django.contrib.auth import login
    import getpass
    import datetime
    """ Email function """
    def decrypted(text):
        from Crypto.Cipher import AES
        from Crypto.Cipher import DES
        import base64
        AES.key_size=128
        key = "5E712B225B5148E9"
        iv = "55FE52A86C3ABWED"
        crypt_object = AES.new(key=key,mode=AES.MODE_CBC,IV=iv)
        original = text
        plain = original.replace('-', "/")
        decoded=base64.b64decode(plain) # your ecrypted and encoded text goes here
        decrypted=crypt_object.decrypt(decoded)
        decrypted = decrypted.decode("utf-8")
        return decrypted
    """" return mail"""
    mail =decrypted(email)
    """ return ip """
    ip = 1
    ip = decrypted(signature)
    """ return time """
    time = decrypted(time)

    now = datetime.datetime.now()
    now_plus_10 = now + datetime.timedelta(minutes = 1)
    time_now = now.strftime('%H:%M')
    date_after_minute = now_plus_10.strftime('%H:%M')

    """ Current ip """
    current_ip = request.META.get('REMOTE_ADDR')
    """" Get url from"""
    URL = request.META.get('HTTP_REFERER')
    referer = None
    if URL:
        referer= URL.split("/")[-3]
    if referer == 'portal.stats.gov.sa':
        if ip == "192..168.2.84":
            if time == time_now or time == date_after_minute:
                username = mail
                try:
                    user = User.objects.get(username=username)
                    #manually set the backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    from django_auth_ldap.backend import LDAPBackend
                    ldap_backend = LDAPBackend()
                    ldap_backend.populate_user(username)
                    # return HttpResponseRedirect(reverse('login'))
                try:
                    user = User.objects.get(username=username)
                    #manually set the backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                except User.DoesNotExist:
                    return HttpResponseRedirect(reverse('login'))
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
                    return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse('login'))

    logged = request.COOKIES.get('logged_in_status')
    context = {'logged':logged, "mail":mail,"ip":ip,"time1":time,"URL":referer}
    template = loader.get_template('project/index.html')
    return HttpResponseRedirect(reverse('ns-project:index'))

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
     # upload file form
    upload = modelformset_factory(Media,form=UploadFile,extra = 1)
    FormSet = upload(queryset=Media.objects.none())

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_obj= form.save(commit=False)
            #default project status
#             try:
#                status_obj= ProjectStatus.objects.get(isdefault=1)
#             except :
#                status_obj= ProjectStatus.objects.order_by('priority')[0]
            project_obj.departement=get_object_or_404(Department, deptcode = request.session.get('DeptCode'))
            project_obj.status=project_obj.status
            project_obj.createdby=get_object_or_404(Employee, empid = request.session.get('EmpID')) 
            project_obj.createddate= datetime.now()
            # if project_obj.end < project_obj.start:
            #     raise ValidationError(_('Invalid date - end date less than start date'))
            #save to database
            project_obj.save()
             #uploading files
            upload_form = upload(request.POST, request.FILES)
            if upload_form.is_valid():
                obj_file = upload_form.save(commit=False)
                for obj in obj_file:
                    obj.project = project_obj
                    if obj.filepath :
                         obj.save()
            else:
                data = {'is_valid': False}
                return JsonResponse(data)
            # redirect to a new URL:
            messages.success(request, _("Project has created successfully"))
            return HttpResponseRedirect(reverse('ns-project:project-list'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project/add_project.html', {'form': form,'upload_file':FormSet,'action_name': _('Ad Project')})

@login_required
def ProjectList(request,project_status=None):
    EmpID = request.session.get('EmpID')
    emp_data  = get_object_or_404(Employee, empid = EmpID)
    dept_data = get_object_or_404(Department, deptcode = request.session.get('DeptCode'))
    tasks_list = Task.objects.filter(assignedto__empid = EmpID)

    if EmpID == dept_data.managerid:
        tasks_list = Task.objects.filter(
        Q(assignedto__empid__exact = EmpID)|
        Q(departement__deptcode__exact  = request.session.get('DeptCode'))
        )
    if project_status =="department":
         tasks_list = Task.objects.filter(
         Q(departement__deptcode__exact = request.session.get('DeptCode'))
         )

    all_project = Project.objects.all()

    project_id = []
    aDict = {}
    allTakProgress = 0
    projectProgress=0
    for data in tasks_list:
        try :
         project_id.append(data.project.id)
        except:
            pass


    project_list= Project.objects.all().filter(
    Q( createdby__exact=EmpID)|
    Q(id__in = project_id)
    ).order_by('-id')

    #check filter by status
    if project_status =="all" :
         project_list=project_list
    elif project_status is not None :
         project_status = project_status.lower()
         project_list=project_list.filter(status__name__contains=project_status)
    if project_status =="department":
        project_list= Project.objects.filter(
        ~Q( createdby__exact=EmpID)&
        Q(id__in = tasks_list)
        )

    for project in project_list:
        task_list = Task.objects.all().filter(project__id= project.id)
        allTakProgress = 0
        for data in task_list:
            if data.progress is not None:
                allTakProgress = allTakProgress + data.progress
            if len(task_list)==0:
                projectProgress=0
            else :
                projectProgress = round(allTakProgress/len(task_list), 2)
            aDict.update({project.id: projectProgress})

    paginator = Paginator(project_list, 10) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)

    context = {'project_list':_plist , 'aDict':aDict,'tasks_list':tasks_list,"project_id":project_id}
    return render(request, 'project/projects.html', context)

@login_required
def ProjectDetail(request,pk):
    project_detail= get_object_or_404(Project,pk=pk)
    EmpID=request.session.get('EmpID')
    tasks_list = Task.objects.filter(project__exact = pk)
    #get all attached files
    attached_files= Media.objects.filter(project__id__exact=pk, task__id__exact=None)
    time_chart = {}
    project_time = []
    for result in _perdelta(project_detail.start, project_detail.end , timedelta(days=7)):
        tasks_list = Task.objects.filter(Q(project__exact = pk,startdate__lte = result)&
        ~Q(status='Closed'))
        # project_time.append(str(result))
        date = result.strftime('%Y,%m,%d')
        now_plus_10 = result - timedelta(days = 30)
        date = now_plus_10.strftime('%Y,%m,%d')
        time_chart.update({str(date): tasks_list.count()})
    #print (date)
    allTakProgress = 0
    projectProgress=0
    project_id = []
    for data in tasks_list:
        project_id.append(data.project.id)
        allTakProgress=allTakProgress+data.progress
    if len(tasks_list)==0:
        projectProgress=0
    else :
        projectProgress=round(allTakProgress/len(tasks_list), 2)


    history=Task.history.filter(project=pk)[:10:1]
    project_list = _get_internal_external_projects( request)
    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'project_detail':project_detail,'project_list':project_list,'current_url':current_url,'projectProgress':projectProgress,
    'taskprogress':allTakProgress,'tasks_list':tasks_list,'history':history,'attached_files':attached_files,
    "time_chart":time_chart}
    return render(request, 'project/project_detail.html', context)

@login_required
def ProjectEdit(request,pk):
    # upload file form
    upload = modelformset_factory(Media,form=UploadFile,extra = 1)
    FormSet = upload(queryset=Media.objects.filter(project__id__exact=pk,task__id__exact=None).exclude(Q(filepath__exact=None)| Q(filepath__exact='')))

    instance = get_object_or_404(Project,pk=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance=form.save()
        instance.save()
         #uploading files
        upload_form = upload(request.POST, request.FILES)
        if upload_form.is_valid():
            obj_file = upload_form.save(commit=False)
            for obj in obj_file:
                obj.project = instance
                if obj.filepath is not None:
                    obj.save()
        else:
            data = {'is_valid': False}

        messages.success(request, _("Project has updated successfully"), fail_silently=True,)
        return HttpResponseRedirect(reverse('ns-project:project-list'))
    else:
        # Set the messages level back to default.
        #messages.add_message(request, messages.ERROR, 'Can not update project.', fail_silently=True, extra_tags='alert')
        #messages.error(request, _("Can not update project."))
        pass
    return render(request, 'project/add_project.html', {'form': form,'upload_file':FormSet,'action_name': _('Edit Project')})

@login_required
def ProjectDelete(request,pk):
    import os
    p= get_object_or_404(Project,pk=pk)
    #get all attached files
    attached_files= Media.objects.filter(project__id__exact=p.id )
    if request.method == 'POST':
        #remove files from directory
        for attached in attached_files :
            os.remove(os.path.join(settings.BASE_DIR, 'media/')+str(attached.filepath))
         #delete attached files related to project and tasks
        try:
             Media.objects.filter(project__id__exact=p.id).delete()
        except:
            pass
         #delete project object and related tasks
        Project.objects.filter(id=p.id).delete()
        messages.success(request, _("Project has deleted successfully"), fail_silently=True,)
        return HttpResponseRedirect(reverse('ns-project:project-list'))
    else:
          context={'p':p,'attached_files':attached_files}
          return render(request, 'project/project_delete.html',context)

@login_required
def ProjectTask(request,pk,task_status=None):
    empDict={}
    dptDict={}
    current_url ="ns-project:" + resolve(request.path_info).url_name
    empid = request.session.get('EmpID')
    project_detail= get_object_or_404(Project,pk=pk)
    tasks_list = Task.objects.filter(assignedto__empid = empid)
    project_id = []
    for data in tasks_list:
        try:
            project_id.append(data.project.id)
        except:
            pass

    project_list= _get_internal_external_projects(request)

    task_list= Task.objects.all().filter(
         Q(project__id__exact=pk)&
         Q(createdby__exact=empid)|
         Q(assignedto__empid__exact = empid,project__id__exact=pk)
         ).order_by('startdate')

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
         date = datetime.today().strftime('%Y-%m-%d')
         task_list= task_list.filter(enddate__lt = date)
         # task_list= task_list.filter(enddate__lt = datetime.today())
    elif task_status=="assignedtodept":
         task_list= task_list.filter(departement__exact= request.session['DeptCode'])


    paginator = Paginator(task_list,10) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        _plist = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _plist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _plist = paginator.page(paginator.num_pages)


    context = {'tasks':_plist,'project_detail':project_detail,'project_list':project_list,'current_url':current_url,'empDict':empDict,'dptDict':dptDict}
    return render(request, 'project/tasks.html', context)

@login_required
def ProjectTaskDetail(request,projectid,taskid):
    assignToEmp=None
    assignToDept=None
    deptcode=request.session['DeptCode']
    #get all attached files
    attached_files= Media.objects.filter(project__id__exact=projectid, task__id__exact=taskid)
    task_detail= get_object_or_404(Task,project_id__exact= projectid,pk=taskid)
    createdby=get_object_or_404(Employee,empid__exact=task_detail.createdby.empid);
    project_list=  _get_internal_external_projects(request)
    current_url ="ns-project:project-task"
    project_detail= get_object_or_404(Project,pk=projectid)



    try:
        assignToEmp=Employee.objects.get(empid__exact=task_detail.assignedto);
    except:
        assignToEmp=None

    try:
       assignToDept=Department.objects.get(deptcode__exact=task_detail.departement.deptcode);
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
               'assignToEmp':assignToEmp,'assignToDept':assignToDept,
               'finishedby':finishedby,
               'cancelledby':cancelledby,
               'closedby':closedby,
               'history':history,
               'attached_files':attached_files
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
            update_change_reason(_obj, _("Update start date for task by")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['notes'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('InProgress')
            data['icon'] = "p_%s" %pk
            data['message'] = _('Start Date Updated successfully')
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
            _obj.finishedby=request.session.get('EmpID')
            _obj.lasteditdate=datetime.now()
            _obj.lasteditby=request.session.get('EmpID')
            _obj.save()
             #add to history
            update_change_reason(_obj, _("Finish Task")+" "+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['notes'])
            data['form_is_valid'] = True
            data['icon'] = "f_"+pk
            data['id'] = pk
            data['status'] = _('Finished')
            data['message'] = _(' Finish Date Updated successfully')
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
            update_change_reason(_obj, _("Close Task by")+request.session['EmpName']+",    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['reason'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Closed')
            data['icon'] = "c_"+pk
            data['message'] = _(' Close Date Updated successfully')
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
            update_change_reason(_obj, _("Cancel Task by ")+request.session['EmpName']+" ,    <i class=\"fa fa-comment\"></i>  " + form.cleaned_data['reason'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Cancelled')
            data['icon'] = "c_%s" %pk
            data['message'] = _('Task has been cancelled successfully')+ pk
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
            update_change_reason(_obj, _("Task Pause by")+ request.session['EmpName'] +",<i class=\"fa fa-comment\"></i>" + form.cleaned_data['note'])
            data['form_is_valid'] = True
            data['id'] = pk
            data['status'] = _('Hold')
            data['icon'] = "c_%s" %pk
            data['message'] = _('Task has been continuous successfully')
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
    project_detail= get_object_or_404(Project,pk=pk)
    tasks= Task.objects.filter(project__id__exact=pk).order_by('startdate')
    project_list = Project.objects.all().filter(
    Q(createdby__exact= request.session.get('EmpID'))|
    Q(id__in = pk)
    ).exclude(status=4).order_by('-id')

    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'tasks':tasks,'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
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
            task_list=task_list.all().exclude(projectid__exact=None)
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
        try:
            projectid.append(data.project.id)
        except:
            pass

    project_list=   project_list = _get_internal_external_projects( request)
    all_emp = VStatisticstaskdata.objects.filter(projectid = project_id)
    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'all_emp':all_emp,'project_detail':project_detail,'project_list':project_list,'current_url':current_url}
    return render(request, 'project/project_team.html', context)

@login_required
def AddTask(request,project_id):
    errors=[]
    data=dict()
    _empname =  request.session['EmpName']
    _deptcode = request.session['DeptCode']
    # upload_file = UploadFile
    upload = modelformset_factory(Media,form=UploadFile,extra = 1)
    FormSet = upload(queryset=Media.objects.none())
    form = AddTaskForm()
    # form.assignedto.queryset = Employee.objects.filter(deptcode = _deptcode)
    form.fields["employee"].queryset = Employee.objects.filter(deptcode = _deptcode)
    if request.method=='POST':
        assignto_employee =  employee=request.POST.get('employee')
        assignto_department =  employee=request.POST.get('department_list')
        form = AddTaskForm(request.POST)
        if form.is_valid():
            # form.save()
            Task_obj = form.save(commit=False)
            Task_obj.project = get_object_or_404(Project,pk=project_id)
            Task_obj.status = 'New'
            Task_obj.createdby = get_object_or_404(Employee,empid__exact=request.session.get('EmpID'))
            Task_obj.lasteditdate = datetime.now()
            Task_obj.createddate = datetime.now()
            Task_obj.progress = 0
            if assignto_employee:
                Task_obj.assignedto =get_object_or_404(Employee,empid__exact=assignto_employee)
                Task_obj.assigneddate = datetime.now()
            if assignto_department:
                Task_obj.departement = get_object_or_404(Department,deptcode__exact=assignto_department)
                Task_obj.assigneddate = datetime.now()
            Task_obj.save()
            #uploading files
            upload_form = upload(request.POST, request.FILES)
            if upload_form.is_valid():
                obj_file = upload_form.save(commit=False)
                for obj in obj_file:
                    obj.project =  Task_obj.project
                    obj.task = Task_obj
                    obj.save()
            else:
                data = {'is_valid': False}
                return JsonResponse(data)
            #update history message
            if assignto_employee:
                assigntodata = get_object_or_404(Employee , empid = assignto_employee )
                update_change_reason(Task_obj, _("Add new Task By")+" " + _empname + " " + _("And Assign to") + " " + assigntodata.empname)
            elif assignto_department:
                assigntodata = get_object_or_404(Department , deptcode__exact = assignto_department )
                update_change_reason(Task_obj, _("Add new Task By") +" " + _empname + " " +_("And Assign to") + " " + assigntodata.deptname)
            else:
                update_change_reason(Task_obj, _("Add new Task By")+" " + _empname)
            #info message
            messages.success(request, _("Task Added"))
            return HttpResponseRedirect(reverse('ns-project:project-task' , kwargs={'pk':project_id} ))

    else:
        data['form_is_valid'] = False
        data['errors'] = errors.append(form.errors)


    context ={'upload_file':FormSet, 'form':form,'action_name':'Add Task','errors':errors}
    return render (request,'project/add_task.html', context)

@login_required
def ProjectTaskDelete(request,projectid,taskid):
    task= get_object_or_404(Task,createdby__empid__exact= request.session['EmpID'],project__id__exact= projectid,pk=taskid)
    project=get_object_or_404(Project,pk=projectid)
    employee=get_object_or_404(Employee,empid__exact= task.createdby.empid)
    if request.method == 'POST':
              Task.objects.filter(id=task.id).delete()
              messages.success(request, _("Task has been deleted successfully"), fail_silently=True,)
              return HttpResponseRedirect(reverse('ns-project:project-task', kwargs={'pk':project.id} ))

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
            #id save == true then save form dta
            if save !="False" :
                 if  employee :
                    _emp_obj=Employee.objects.get(empid__exact= int(form.cleaned_data['employee'].empid))
                    _obj.assignedto=_emp_obj
                    _assign=form.cleaned_data['employee'].empname
                    _obj.departement=get_object_or_404(Department,deptcode__exact= _emp_obj.deptcode)
                    _receiver=_emp_obj.email

                 elif departement :
                    _dpt_obj=Department.objects.get(deptcode__exact= int(form.cleaned_data['departement'].deptcode))
                    _obj.departement=_dpt_obj
                    _assign=form.cleaned_data['departement'].deptname
                    _obj.assignedto=None
                    #manager
                    manager_obj=Employee.objects.get(empid__exact= int(_dpt_obj.managerid))
                    _receiver=manager_obj.email
                 _obj.assigneddate=datetime.now()
                 _obj.cancelleddate=None
                 _obj.cancelledby=None
                 _obj.closeddate=None
                 _obj.closedby=None
                 _obj.finisheddate=None
                 _obj.finishedby=None
                 _obj.lasteditdate=datetime.now()
                 _obj.save()
                #add to history
                 update_change_reason(_obj,_(" by ")+ request.session['EmpName'] +"  ," +  _("Assign Task to")+  str(_assign))
                 messages.success(request, "<i class=\"fa fa-check\" aria-hidden=\"true\"></i>"+_("Assign Task to")+"  "+_assign, fail_silently=True,)
                 #send email notification
                 if _receiver is not None :
                     try:
                         message=_obj.name+'<br><a href="http://'+request.get_host()+'/project/project_task_detail/'+str(_obj.project.id)+'/'+str(_obj.id)+'">'+_('Click Here')+'</a>'
                         message=message+'<br>'+_(" by ")+request.session['EmpName'] +"<br>" +  _("Assign Task to")+  str(_assign)+_(' in ')+str(_obj.assigneddate)
                         subject =_('Task has been asigned to you')
                         #str(_obj.assignedto.email) to be add in next line
                         send_mail(subject,message,'sakr@stats.gov.sa',['sakr@stats.gov.sa'],fail_silently=False,html_message=message,)
                     except:
                         pass
            data['form_is_valid'] = True
            data['id'] = pk
            data['message'] = "<i class=\"fa fa-check\" aria-hidden=\"true\"></i>" + _('Task has been assigned successfully')
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
    errors = []
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
        data['errors'] = errors.append(form.errors)

    # if a GET (or any other method) we'll create a blank form
    context = {'form': form,'pk':pk,'errors':errors}
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

    # upload file form
    upload = modelformset_factory(Media,form=UploadFile,extra = 1,can_delete=True)
    FormSet = upload(queryset=Media.objects.filter(project_id__exact=projectid,task__id__exact=taskid).exclude(Q(filepath__exact=None)| Q(filepath__exact='')))

    try:
        form.fields["assigned_to"].initial=task_detail.assignedto.empid
    except:
        pass
    try:
        form.fields["assigned_to"].initial=task_detail.departement.deptcode
    except:
        pass

    # for use in futrure
    #form.fields["createdby"].queryset = Employee.objects.filter(deptcode = request.session['DeptCode'])
    #form.fields["createdby"].initial=task_detail.createdby

    try:
        assignTo=empid__exact=task_detail.assignedto.empname;
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
        instance=form.save(commit=False)
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

        #check if user select employee or dept or do nothing

        try:
            instance.assignedto= Employee.objects.get(empid__exact= int(form.cleaned_data['assigned_to']))
        except:
            instance.assignedto=None
        try:
            instance.departement= Department.objects.get(deptcode__exact= int(form.cleaned_data['assigned_to']))
        except:
            instance.departement=None

        instance.lasteditdate=datetime.now()
        instance.lasteditby=request.session['EmpID']
        instance.save()
        #uploading files
        upload_form = upload(request.POST, request.FILES)
        if upload_form.is_valid():
            obj_file = upload_form.save(commit=False)
            for obj in obj_file:
                obj.project = instance.project
                obj.task=instance
                if obj.filepath is not None or obj.filepath !="":
                    obj.save()
                else:
                   obj.delete()
        else:
            data = {'is_valid': False}
        messages.success(request, _(" Task has been updated successfully "), fail_silently=True,)
        #add to history
        update_change_reason(instance, _("Edit Task successfully by")+" : "+  str( employee.empname)+ ( ",    <i class=\"fa fa-comment\"></i>  "+ form.cleaned_data['note']  if form.cleaned_data['note'] else " "))
        return HttpResponseRedirect(reverse('ns-project:project-task-detail', kwargs={'projectid':projectid,'taskid':taskid}))
    else:
        context = {'project_detail':project_detail,
               'project_list':project_list,
               'current_url':current_url,
               'task':task_detail,
               'form':form,
               'upload_file':FormSet,
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
    tasks_list = Task.objects.filter(assignedto__empid = empid)
    project_id = []
    for data in tasks_list:
        try:
            project_id.append(data.project.id)
        except:
            pass
    #no of new task
    new_tasks_count= len(Task.objects.all().filter(Q(status__exact='New')&(
         Q(assignedto__empid__exact = empid)|Q(departement__deptcode__exact =  request.session['DeptCode']))
         ).exclude(createdby__exact=empid))

    #get all tasks assign to dept from external project
    task_list= Task.objects.all().filter(
         Q(departement__deptcode__exact=  request.session['DeptCode'])
         ).exclude(createdby__exact=empid).order_by('-id')


    if task_status=="all":
         task_list= task_list

    elif task_status=="unclosed":
         task_list = task_list.exclude(status__exact='Closed')
    elif task_status=="assignedtome":
         task_list= task_list.filter(assignedto__empid__exact=empid)
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
         date = datetime.today().strftime('%Y-%m-%d')
         task_list= task_list.filter(enddate__lt = date)
    elif task_status=="assignedtodept":
         task_list= task_list.filter(departement__deptcode__exact= request.session['DeptCode'])


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

@login_required
def DashboardManager(request):
    from dateutil.relativedelta import relativedelta
    from django.db.models import F
    dept_code  = request.session['DeptCode']
    start_date = datetime.now() - relativedelta(years=1)
    end_date = datetime.now()
    task_based_department = dept_task_indicators(dept_code,start_date,end_date)
    pie_tasks=_dept_tasks_statistics(dept_code,start_date,end_date)
    open_projects=_dept_open_pojects(dept_code,start_date,end_date)
    per_indicator = indicators(dept_code,start_date,end_date)
    project_kpi=_project_kpi(dept_code, start_date, end_date)
    open_tasks=_open_tasks(dept_code, start_date, end_date)
    context = {"start_date":start_date,"end":end_date,"task_based_department":task_based_department,
               'pie_tasks':pie_tasks,"per_indicator":per_indicator,'open_projects':open_projects,'project_kpi':project_kpi,
               'open_tasks':open_tasks
               }
    return render(request, 'project/dashboard_manager.html', context)

@login_required
def DashboardEmployee(request,empid):
    from dateutil.relativedelta import relativedelta
    dept_code  = request.session['DeptCode']
    start_date = datetime.now() - relativedelta(years=1)
    end_date = datetime.now()
    employee= get_object_or_404(Employee,empid__exact=empid)
    task_employee = emp_task(empid,start_date,end_date)
    kpi= _project_kpi_employee(employee,start_date,end_date)
    pie_tasks=_employee_tasks_statistics(employee,start_date,end_date)
    context = {"task_employee":task_employee,'employee':employee,'kpi':kpi,'pie_tasks':pie_tasks}
    return render(request, 'project/dashboard_employee.html', context)

def emp_task(empid,start_date,end_date):
    task_employee = Task.objects.filter(
    Q(assignedto__empid__exact = empid)&
    Q(startdate__gte = start_date, startdate__lte = end_date)&
    ~Q(status ='Closed')
    )
    return task_employee

def dept_task_indicators(dept_code,start_date,end_date):
    dept_data = get_object_or_404(Department,deptcode=dept_code)
    dept_manager = dept_data.managerid
    dept_internal_task_count = Task.objects.filter(
    Q(createdby = dept_manager)&
    Q(enddate__gte = start_date, startdate__lte = end_date)
    ).count()

    dept_external_task = Task.objects.filter(
    Q(departement = dept_code)&
    ~Q(createdby = dept_manager)&
    Q(enddate__gte = start_date, startdate__lte = end_date)
    )

    TaskDict = {}
    TaskDict.update({dept_data.deptname: dept_internal_task_count})
    for data in dept_external_task:
        tasks = Task.objects.filter(departement = data.departement, createdby = data.createdby)
        task_count = tasks.count()
        for name in tasks:
            each_dept_count = tasks.filter(createdby = name.createdby).count()
            TaskDict.update({name.createdby.deptname: each_dept_count})
    return TaskDict

def _dept_tasks_statistics(deptcode,startdate,enddate):
    tasks = {}
    task_list= Task.objects.filter(project__departement__deptcode__exact=deptcode,createddate__gte=startdate,createddate__lte=enddate)
    tasks['New']=task_list.filter(status__exact='New').count()
    tasks['InProgress']=task_list.filter(status__exact='InProgress').count()
    tasks['Done']=task_list.filter(status__exact='Done').count()
    tasks['Hold']=task_list.filter(status__exact='Hold').count()
    tasks['Canceled']=task_list.filter(status__exact='Canceled').count()
    tasks['Closed']=task_list.filter(status__exact='Closed').count()
    return tasks

def _dept_open_pojects(deptcode,startdate,enddate):

    projectList=[]
#     new = Count('task', distinct=True, filter=Q(status__exact="Done"))
#     inprogress = Count('task', distinct=True, filter=Q(task__status__exact="InProgress"))
#     done = Count('task', distinct=True, filter=Q(task__status__exact="Done"))
#     hold = Count('task', distinct=True, filter=Q(status__exact="Hold"))
#     closed = Count('task', distinct=True, filter=Q(status__exact="Closed"))
    projects= Project.objects.filter(
        (Q(departement__deptcode__exact=deptcode) & Q(start__gte=startdate) & Q(start__lte=enddate))
        & ~Q(status__name__exact="Closed")).annotate(num_tasks=Count('task'))

    q=projects.query
    for project in projects :
        projectDict={}
        tasks=Task.objects.filter(project__id=project.id)
        projectDict["detail"]=project
        if project.end <= datetime.date(datetime.now()) :
             projectDict["commitment"]=True
        else:
             projectDict["commitment"]=False
        projectDict["All"]=project.num_tasks
        projectDict["Progress"]=tasks.aggregate(Avg('progress'))
        projectDict["New"]=tasks.filter(status__exact="New").count()
        projectDict["Done"]=tasks.filter(status__exact="Done").count()
        projectDict["Closed"]=tasks.filter(status__exact="Closed").count()
        projectDict["Canceled"]=tasks.filter(status__exact="Canceled").count()
        projectDict["Hold"]=tasks.filter(status__exact="Hold").count()
        projectDict["InProgress"]=tasks.filter(status__exact="InProgress").count()
        projectList.append(projectDict)
    return projectList


def _project_kpi(deptcode,startdate,enddate):
    projectKPI={}
    projects= Project.objects.filter(
        (Q(start__gte=startdate)& Q(start__lte=enddate))&
                                       (Q(departement__deptcode__exact=deptcode)| Q(task__departement__deptcode__exact=deptcode))
                                    ).annotate(dcount=Count('departement'))
    projectKPI["p_all"]= projects.count()
    projectKPI["p_internal"]= projects.filter(departement__deptcode__exact=deptcode).count()
    projectKPI["p_external"]= projects.filter( Q(task__departement__deptcode__exact=deptcode) & ~Q(departement__deptcode__exact = deptcode)).count()

    tasks=Task.objects.filter(
        (Q(startdate__gte=startdate)& Q(startdate__lte=enddate))&
                                       (Q(departement__deptcode__exact=deptcode)| Q(project__departement__deptcode__exact=deptcode))
                                    )
    projectKPI["t_all"]= tasks.count()
    projectKPI["t_internal"]= tasks.filter(  Q(project__departement__deptcode__exact=deptcode)).count()
    projectKPI["t_external"]= tasks.filter(  Q(departement__deptcode__exact=deptcode) & ~Q(project__departement__deptcode__exact=deptcode)).count()
    return projectKPI


def _open_tasks(deptcode,startdate,enddate):
    openTasks= Task.objects.filter(
      (Q(departement__deptcode__exact= deptcode) | Q(project__departement__deptcode__exact= deptcode))
        & ~Q(status__exact="Closed"))
    return openTasks


def indicators(deptcode,start_date,end_date):
    from django.db.models import F
    #all task from now and 12 monthes before
    all_task = Task.objects.filter(
    (Q(project__departement__deptcode = deptcode) | Q(departement__deptcode = deptcode))&
    Q(startdate__gte = start_date, startdate__lte = end_date)
    )
    all_task_count = all_task.count()

    task_done = all_task.filter(
   ( Q(status__exact = 'Closed') | Q(status__exact = 'Done'))
    ).order_by("enddate").filter(enddate__gte = F('finisheddate')).count()

    task_delayed = all_task_count - task_done
    try :
        per_indicator = round(task_done/all_task_count*100)
    except:
       per_indicator=0
    return per_indicator
#download attached file from media
def Download(request,file_name):
    from wsgiref.util import FileWrapper
    import mimetypes
    import os
    import django.utils.encoding

    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' %file_name
    return response

#kanban view
def Kanban (request,pk):
    project_detail= get_object_or_404(Project,pk=pk)
    tasks= Task.objects.filter(project__id__exact=pk).order_by('startdate')
    new_tasks=tasks.filter(status__exact="New")
    inprogress_tasks=tasks.filter(status__exact="Inprogress")
    done_tasks=tasks.filter(status__exact="Done")
    hold_tasks=tasks.filter(status__exact="Hold")
    cancelled_tasks=tasks.filter(status__exact="Cancelled")
    closed_tasks=tasks.filter(status__exact="Closed")
    project_list = Project.objects.all().filter(
    Q(createdby__exact= request.session.get('EmpID'))|
    Q(id__in = pk)
    ).exclude(status=4).order_by('-id')

    current_url ="ns-project:" + resolve(request.path_info).url_name
    context={'tasks':tasks,'project_detail':project_detail,'project_list':project_list,'current_url':current_url,'new_tasks':new_tasks,'inprogress_tasks':inprogress_tasks,'done_tasks':done_tasks,'hold_tasks':hold_tasks,'cancelled_tasks':cancelled_tasks,'closed_tasks':closed_tasks}
    return render(request, 'project/kanban.html', context)

#test email
def senmail(request) :
    send_mail(
    'Subject here',
    'Here is the message.',
    'sakr@stats.gov.sa',
    ['sakr@stats.gov.sa'],
    fail_silently=False,

    )
    context={}
    return render(request, 'project/plain_page.html', context)

#Delegation for timesheet#
@login_required
def adddelegation(request):
    form = AddDelegation
    if request.method=='POST':
        auth_employee = request.POST.get('employee', False)
        print ('is Post')
        form = form(request.POST)
        if form.is_valid():
            print ('is valid')
            obj = form.save(commit = False)
            obj.authorized = get_object_or_404(Employee,empid__exact=auth_employee)
            obj.managerid =  get_object_or_404(Employee,empid__exact=request.session.get('EmpID'))
            obj.deptcode = get_object_or_404(Department,deptcode__exact=obj.managerid.deptcode)
            aut_data = get_object_or_404(Employee,empid__exact=auth_employee)
            obj.deptauthcode = aut_data.deptcode
            obj.expired = '0'
            obj.save()
            messages.success(request, _("Add complete"))
            return HttpResponseRedirect(reverse('ns-project:delegation'))
    else:
        form = form
    context = {"form":form}
    return render(request, 'project/add_delegation.html', context)

@login_required
def editdelegation(request,pk):
    EmpID = request.session.get('EmpID')
    record = get_object_or_404(Delegation, pk=pk)
    form = AddDelegation
    if EmpID == record.managerid.empid:
        form = form(request.POST or None, instance=record)
        form.fields["employee"].initial=record.authorized.empid
        if request.method=='POST':
            auth_employee = request.POST.get('employee', False)
            print ('is Post')
            if form.is_valid():
                print ('is valid')
                obj = form.save(commit = False)
                obj.authorized = get_object_or_404(Employee,empid__exact=auth_employee)
                obj.managerid =  get_object_or_404(Employee,empid__exact=request.session.get('EmpID'))
                obj.deptcode = get_object_or_404(Department,deptcode__exact=obj.managerid.deptcode)
                aut_data = get_object_or_404(Employee,empid__exact=auth_employee)
                obj.deptauthcode = aut_data.deptcode
                obj.save()
                messages.success(request, _("Edit complete"))
                return HttpResponseRedirect(reverse('ns-project:delegation'))
        else:
            form = form
    else:
        raise Http404

    context = {"form":form}
    return render(request, 'project/edit_delegation.html', context)

@login_required
def delegation(request):
    if request.user.is_authenticated():
        EmpID = request.session.get('EmpID',0)
    all_delegations = Delegation.objects.filter(managerid = EmpID).order_by('expired')
    count = len(list(all_delegations))
    if count == 0:
        messages.info(request, _("No Delegations"))
    context = {'AllDelegations': all_delegations,'count':count}
    return render(request, 'project/delegation.html', context)

@login_required
def mydelegation(request):
    if request.user.is_authenticated():
        EmpID = request.session.get('EmpID',0)
    all_delegations = Delegation.objects.filter(authorized = EmpID, expired = '0')

    count = len(list(all_delegations))
    if count == 0:
        messages.info(request, _("No Delegations"))
    context = {'AllDelegations': all_delegations,'count':count}
    return render(request, 'project/my_delegation.html', context)

def _get_internal_external_projects(request):
    deptcode = request.session['DeptCode']
    if request.user.groups.filter(name="ismanager").exists():
         projects=Project.objects.filter(
             (Q(task__project__departement__deptcode__exact=deptcode)| Q(task__departement__deptcode__exact=deptcode))
                                        ).annotate(dcount=Count('task')).order_by('-id')
    else:
       projects=Project.objects.filter(
             ( Q(task__assignedto__empid__exact=request.session['EmpID']))
                                        ).annotate(dcount=Count('task')).order_by('-id')
    return projects

def _project_kpi_employee(employee,startdate,enddate):
    projectKPI={}
    projects= Project.objects.filter(
        (Q(start__gte=startdate)& Q(start__lte=enddate))&
                                       ( Q(task__assignedto__empid__exact=employee.empid))
                                    ).annotate(dcount=Count('task'))
    projectKPI["p_all"]= projects.count()
    projectKPI["p_internal"]= projects.filter(departement__deptcode__exact=employee.deptcode).count()
    projectKPI["p_external"]= projects.filter(  ~Q(departement__deptcode__exact = employee.deptcode)).count()

    tasks=Task.objects.filter(
        (Q(startdate__gte=startdate)& Q(startdate__lte=enddate))&
                                       (Q(assignedto__empid__exact=employee.empid))
                                    )
    projectKPI["t_all"]= tasks.count()
    projectKPI["t_internal"]= tasks.filter(  Q(project__departement__deptcode__exact=employee.deptcode)).count()
    projectKPI["t_external"]= tasks.filter(   ~Q(project__departement__deptcode__exact=employee.deptcode)).count()
    return projectKPI

def _employee_tasks_statistics(employee,startdate,enddate):
    tasks = {}
    task_list= Task.objects.filter(assignedto__deptcode__exact=employee.deptcode,startdate__gte=startdate,startdate__lte=enddate)
    tasks['New']=task_list.filter(status__exact='New').count()
    tasks['InProgress']=task_list.filter(status__exact='InProgress').count()
    tasks['Done']=task_list.filter(status__exact='Done').count()
    tasks['Hold']=task_list.filter(status__exact='Hold').count()
    tasks['Canceled']=task_list.filter(status__exact='Canceled').count()
    tasks['Closed']=task_list.filter(status__exact='Closed').count()
    return tasks

def _get_tree_dept(deptcode):
    dept_level_1 = ApfDeptView.objects.filter(resp_dept_code = deptcode)
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
    all_dept.append(deptcode)
    return all_dept

def _perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def ProjectReport(request,selectedDpt=None):
    _rtype=None
    _rlist=[]
    deptcode= request.session['DeptCode']
    departement_list= ApfDeptView.get_all_children(deptcode)
    #chek if user has authticat to see selected deptcode
    if len(departement_list) > 1 :
        departement_list.pop(0)
    try:
        for dept in departement_list:
            if dept.dept_code == selectedDpt :
                deptcode = selectedDpt
    except:
        pass

    print(deptcode)
    project_list= Project.objects.filter(( Q(departement__deptcode__exact=deptcode))).order_by('-id')

    #intiat form

    form = ReportForm()
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = ReportForm(request.POST)

        form.fields["project"].queryset =project_list
        if form.is_valid():
            _rtype=form.cleaned_data['reportType']
            _project=form.cleaned_data['project']
            tasks=Task.objects.filter( Q(project__id__exact=_project.id) & (Q(departement__deptcode__exact=deptcode)| Q(project__departement__deptcode__exact=deptcode))
                                    )
            for type in _rtype :

                #report project
                if type == "project" :
                    Dict={}
                    Dict['type']="project"
                    Dict['project']=_project

                    Dict['taskCount'] =tasks.count()
                    Dict['progress']=tasks.aggregate(Avg('progress'))
                    Dict['internal']=tasks.filter(Q(departement__deptcode__exact=deptcode) | (Q(departement__deptcode__exact=None)) & Q(project__departement__deptcode__exact=deptcode)).count()
                    Dict['external']=tasks.filter(~Q(departement__deptcode__exact=deptcode)).count()

                    _rlist.append(Dict)
                #report task assigned to
                if type == "assignedto" :
                    Dict={}
                    Dict["all"]=tasks.count()
                    Dict['type']="assignedto"
                    assignedto= tasks.values('assignedto__empname').annotate( num_assign=Count('assignedto')).exclude(Q(assignedto__exact=None))
                    notasigned= tasks.filter(Q(assignedto__exact=None) & Q(departement__exact=None)).count()
                    assignto_dept= tasks.values('departement__deptname').annotate( num_assign=Count('departement')).exclude(Q(departement__exact=None))
                    _assignedto_list=[]
#                     for assign in assignedto :
#                         _assignedto_list["assign_to"]=assign
#                         _assignedto_list["num_assign"]=assign.num_assign
#                         _assignedto_list["precent"]=assign.num_assign/ Dict["all"]
#
                    Dict["assignedto"]=assignedto
                    Dict["notasigned"]=notasigned
                    Dict["assignto_dept"]=assignto_dept
                    _rlist.append(Dict)

                 #report task status
                if type == "status" :
                    Dict={}
                    Dict['type']="status"
                    Dict["all"]=tasks.count()
                    _status_list=['New','Done','Closed','Canceled','Hold','InProgress']
                    status_list=[]
                    for status in _status_list:
                        statusDict={}
                        statusDict['name']=status
                        statusDict['count']=tasks.filter(status__exact=status).count()
                        if Dict["all"] !=0 :
                            statusDict['precent']=(statusDict['count']/Dict["all"])*100
                        else :
                            statusDict['precent']=0
                        status_list.append(statusDict)
                    Dict["status"]=status_list
                    _rlist.append(Dict)

    depObject=  get_object_or_404(ApfDeptView, dept_code__exact= request.session['DeptCode'])
    print(depObject)
    form.fields["project"].queryset =project_list
    context={'form':form,'rtype':_rtype,'rlist':_rlist,'project_list':project_list,'departement_list':departement_list,'selectedDpt':selectedDpt,'depObject':depObject}
    return render(request, 'project/reports/project_report.html', context)
