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



class ProjectAdmin(admin.ModelAdmin):
    model = Project
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

admin.site.register(Project,ProjectAdmin)
