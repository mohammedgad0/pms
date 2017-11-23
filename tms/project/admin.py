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

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
