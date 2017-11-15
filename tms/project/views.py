from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Employee
from .forms import *
from django.contrib.auth.views import *
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.forms import formset_factory


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
            request.session['DepName'] = data.depname
            request.session['Mobile'] = data.mobile
            request.session['DeptCode'] = data.depcode
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

def AddSheet(request):
    form = formset_factory(AddNewSheet, extra=6)
    formset = form
    # form = AddNewSheet
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
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project/add_project.html', {'form': form})
