from json import loads

from django.http.response import JsonResponse, HttpResponseNotAllowed
from .forms import AddPhaseForm
from .models import Department, Employee


def add_phase(request):
    data = loads(request.body)

    if request.method == 'POST':
        form = AddPhaseForm(data)

        if form.is_valid():
            saved = form.save(commit=False)
            saved.department = Department.objects.get(deptcode=request.session['DeptCode'])
            saved.created_by = Employee.objects.get(empid=request.session['EmpID'])
            saved.save()

            if not saved.id:
                return JsonResponse({'status': 0, 'message': 'حدث خطأ أثناء عملية الحفظ'})

            return JsonResponse({'status': 1, 'data': {'pk': saved.id, 'name': saved.name}})
        else:
            return JsonResponse({'status': 0, 'message': [value[0] for key, value in form.errors.items()][0]})
    else:
        return HttpResponseNotAllowed()
