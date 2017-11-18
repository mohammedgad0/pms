from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Project 
from django.http import HttpResponse
from django.core import serializers

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect



class ProjectAdmin(admin.ModelAdmin):
    model = Project
    fk_name = "id"

admin.site.register(Project,ProjectAdmin)