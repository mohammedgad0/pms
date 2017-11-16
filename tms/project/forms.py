from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import modelformset_factory
from .models import *


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class AddNewSheet(forms.Form):
    TaskDesc = forms.CharField(label=_("Task Descreption"),
               widget=forms.TextInput({'class': 'form-control','placeholder': 'وصف المهمة كامل'}))

    TaskType = forms.ChoiceField(choices=(('M', _('Master')), ('H', _('Help'))),label=_("Task type"),
                    widget=forms.Select({'class': 'form-control','placeholder':'task'}))
    Duration = forms.IntegerField(label=_("Duration"),
               widget=forms.NumberInput({'class': 'form-control','placeholder':'0'}))

AddSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration'))

class ProjectForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    ProjectName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_('project Name')}))
    StartDay = forms.DateField(initial=datetime.date.today,widget=forms.TextInput(attrs={'class': 'form-control xdisplay_inputx form-group has-feedback','id':'single_cal1','placeholder':_('Start Date')}))
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
