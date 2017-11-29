from django.contrib.auth.models import User
import django_filters
from .models import *
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import modelformset_factory
from .models import *
from django.forms import ModelForm, Textarea,TextInput,DateField


class SheetFilter(django_filters.FilterSet):
    class Meta:
        model = Sheet
        fields = ['tasktype', 'ifsubmitted', 'status','taskdate']
