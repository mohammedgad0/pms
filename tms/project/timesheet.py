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
from .defs import test
from simple_history.utils import update_change_reason

@login_required
@permission_required('project.add_sheet',raise_exception=True)
def MySheet(request):

    EmpID = 0
    if request.user.is_authenticated():
        EmpID = request.session['EmpID']
    sheets = Sheet.objects.filter(empid = EmpID).order_by('ifsubmitted','status')
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
    EmpID = request.session.get('EmpID')
    deptcode = EmpData.deptcode
    alldept = request.session.get('TreeDept', '0')
    delegation = Delegation.objects.filter(authorized = EmpID, expired = '0')
    auth_dept = []
    for data in delegation:
        auth_dept.append(data.deptcode.deptcode)
    have_permission = False
    if int(deptcode) in auth_dept:
        have_permission = True
    his_manager = False
    if str(EmpData.managercode) == str(request.session['EmpID']):
        his_manager = True
    if str(EmpData.managercode) == str(request.session['EmpID']) or deptcode in alldept or have_permission:
        sheet_list = Sheet.objects.filter(empid = empid).order_by('ifsubmitted','status')
        start = request.GET.get("q_start")
        end = request.GET.get("q_end")
        if start:
            sheet_list = Sheet.objects.filter(empid = empid,taskdate__gte=start, taskdate__lte=end)
        # EmpData = Employee.objects.filter(empid = empid)
        sheet_filter = SheetFilter(request.GET, queryset=sheet_list)
    else:
        raise Http404

    return render(request, 'project/emp_sheet.html', {'have_permission':have_permission,'filter': sheet_filter,'EmpData':EmpData,"his_manager":his_manager})

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
    alldept = request.session.get('TreeDept', '0')
    for data in dept:
        managid = data.managerid
    delegation = Delegation.objects.filter(authorized = EmpID, expired = '0')
    auth_dept = []
    for data in delegation:
        auth_dept.append(data.deptcode.deptcode)
    have_permission = False
    if int(deptcode) in auth_dept:
        have_permission = True
    if managid == EmpID or deptcode in alldept or have_permission:
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
    context = {'allemp':AllEmp,"count":count,"total_task":total_task,"delgation":auth_dept,
    "have_permission":have_permission,
    "submitted_task":submitted_task,"n_task":not_submitted_task,"emp_count":emp_count}
    if count == 0:
        messages.info(request, _("No data"))
        return render(request, 'project/all_sheets.html',context)

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
