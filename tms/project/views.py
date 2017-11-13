from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Employee
from .forms import *
from django.contrib.auth.views import *
from django.http import HttpResponseRedirect


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
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    context = {'username'}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('project/' + load_template)
    return HttpResponse(template.render(context, request))
