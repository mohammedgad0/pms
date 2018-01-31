from django.conf import settings
from django.utils import translation
from .models import *
from django.contrib.auth.models import Group
from django.http import HttpResponse ,HttpResponseRedirect,Http404 ,HttpResponseForbidden
class ForceLangMiddleware:
    def process_request(self, request):
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG
        if request.user.is_authenticated():
            # if not request.session['EmpID']:
            email = request.user.email
            try:
                emp = Employee.objects.filter(email= email).get()
                if emp is not None:
                    request.session['EmpID'] = emp.empid
                    request.session['Email'] = emp.email
                    request.session['EmpName'] = emp.empname
                    request.session['DeptName'] = emp.deptname
                    request.session['Mobile'] = emp.mobile
                    request.session['DeptCode'] = emp.deptcode
                    request.session['JobTitle'] = emp.jobtitle
                    request.session['IsManager'] = emp.ismanager
                
                    if emp.ismanager == 1:
                            g = Group.objects.get(name='ismanager')
                            g.user_set.add(request.user.id)
                    else:
                            g = Group.objects.get(name='employee')
                            g.user_set.add(request.user.id)
                    obj_emp = Delegation.objects.filter(authorized = emp.empid , expired="0")
                    if obj_emp:
                        request.session['have_auth']  = True
            except:
                 pass
           
class UserSeesionSet:
    def UserSessions(request):
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
