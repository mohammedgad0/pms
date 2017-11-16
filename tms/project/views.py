from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Employee
from .forms import *
from django.contrib.auth.views import *
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.forms import formset_factory
from .models import *
from django.forms import BaseModelFormSet


def myuser(request, *args, **kwargs):
    if request.method == "POST":
        form = BootstrapAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # email = None
            # if request.user.is_authenticated():
            email = request.user.email
            emp = Employee.objects.filter(email= email)
    # Get all data filtered by user email and set in session
        for data in emp:
            request.session['EmpEmail'] = data.email
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

# @login_required
def AddSheet(request):
    AddSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration'), extra=4,
        widgets = {
            'taskdesc': forms.TextInput(attrs={'class': 'form-control'}),
            'tasktype': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    )

    if request.method == 'POST':
        formset = AddSheet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for obj in instances:
                obj.createddate = datetime.datetime.now()
                obj.save()
    else:
        formset = AddSheet()
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
            p_obj= Project(name=ProjectName,start=StartDate,end=EndDate,desc=Desc)
            p_obj.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project/add_project.html', {'form': form})
