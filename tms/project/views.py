from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Employee

def index(request):
    email = None
    if request.user.is_authenticated():
        email = request.user.email
        emp = Employee.objects.filter(email= email)
# Get all data filtered by user email and set in session
        for data in emp:
            request.session['EmpEmail'] = data.email
            request.session['EmpName'] = data.empname
            request.session['DepName'] = data.depname
            request.session['Mobile'] = data.mobile
            request.session['DeptCode'] = data.depcode

    context = {}
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
