from django.conf import settings
from django.utils import translation
from .models import *
class ForceLangMiddleware:

    def process_request(self, request):
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG
        if request.user.is_authenticated():
            if not request.session['EmpID']:
                email = request.user.email
                emp = Employee.objects.filter(email= email)
                # Get all data filtered by user email and set in session
                for data in emp:
                    request.session['EmpID'] = data.empid
                    request.session['EmpName'] = data.empname
                    request.session['DeptName'] = data.deptname
                    request.session['Mobile'] = data.mobile
                    request.session['DeptCode'] = data.deptcode
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
