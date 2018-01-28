from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import *
from django.http import HttpResponse
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

admin.site.site_title = _('Project Management System cp')
admin.site.site_header = _('Project Management System cp')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    fk_name = "id"

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    model = ProjectStatus
    fk_name = "id"


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ['filename']
    def get_task(self, obj):
        return obj.Task.name
    get_task.admin_order_field  = 'taskid'  #Allows column order sorting
    get_task.short_description = 'Task Name'  #Renames column head

    #Filtering on side - for some reason, this works
    #list_filter = ['title', 'author__name']

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class SheetAdmin(admin.ModelAdmin):
    model = Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    fk_name = "id"
    fields = ( 'empname', 'sexcode', 'empid', 'jobtitle', 'deptcode', 'deptname', 'mobile', 'email','ismanager','managercode','ext','iscontract')
    list_display =( 'empname', 'empid', 'jobtitle', 'deptcode', 'deptname',  'email','ismanager','managercode','ext','iscontract')
  #  filter_vertical=('deptcode','sexcode')
    list_filter=('ismanager','iscontract')
    #list_max_show_all=200
    list_per_page=100
    ordering = ['-ismanager','empname']
    search_fields = ['empname', 'sexcode', 'empid', 'jobtitle', 'deptcode', 'deptname', 'mobile', 'email']
   # autocomplete_fields=['empname']  #autocomplete_fields is a list of ForeignKey and/or ManyToManyField fields
    show_full_result_count=True
    

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    fk_name = "id"
    fields = ( 'deptname', 'managerid', 'deptcode')
    list_display = ( 'deptname', 'managerid', 'deptcode')
    list_per_page=100
    ordering = ['-deptcode',]
    search_fields = ['deptname', 'managerid', 'deptcode']
    show_full_result_count=True