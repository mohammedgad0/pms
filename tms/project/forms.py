from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import modelformset_factory
from .models import *
from django.forms import ModelForm, Textarea,TextInput,DateField

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': _('User Name')}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':_('Password')}))

class AddNewSheet(forms.Form):
    TaskDesc = forms.CharField(label=_("Task Descreption"),
               widget=forms.TextInput({'class': 'form-control','placeholder': 'وصف المهمة كامل'}))

    TaskType = forms.ChoiceField(choices=(('M', _('Master')), ('H', _('Help'))),label=_("Task type"),
                    widget=forms.Select({'class': 'form-control','placeholder':'task'}))
    Duration = forms.IntegerField(label=_("Duration"),
               widget=forms.NumberInput({'class': 'form-control','placeholder':'0'}))

UpdateSheet = modelformset_factory(Sheet, fields=('taskdesc', 'tasktype', 'duration'))

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['name','start','end','desc']
        widgets = {
            'name':TextInput(attrs={'class': 'form-control','placeholder':_('Project Name'),'required': True}),
            'start':TextInput(attrs={'class': 'form-control has-feedback-left  ','id':'single_cal_1','aria-describedby':'inputSuccess2Status','placeholder':_('Start Date'),'required': True}),
            'end':TextInput(attrs={'class': 'form-control has-feedback-left  ','id':'single_cal_2','aria-describedby':'inputSuccess2Status','placeholder':_('End Date'),'required': True}),
            'desc': Textarea(attrs={'class':'form-control','placeholder':_('Project Details'),'required': True}),
        }
        labels = {
            'name': _('Project Name'),
            'start':_('Start Date'),
            'end':_('End Date'),
            'desc':_('Desc'),
        }
        help_texts = {
            'desc': _('write a Description for Project .'),
            'start':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
            'end':_('Please use the following format: <em>YYYY-MM-DD</em>.'),
        }
        error_messages = {
            'name': {
                    'max_length': _("The Project's name is too long."),
                    'required': _("Project's name is required."),
             },
            'start': {
                    'required': _("Start Date  is required."),
             },
            'end': {
                    'required': _("End Date  is required."),
             },
            'desc': {
                    'max_length': _("The Project's Description is too long."),
                    'required': _("Description Date  is required."),
             },
        }
