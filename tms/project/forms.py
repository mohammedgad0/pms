from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
import datetime

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
               


class ProjectForm(forms.Form):
    ProjectName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':_('Project Name')}))
    StartDate= forms.DateField(initial=datetime.date.today,widget=forms.TextInput(attrs={'class': 'form-control xdisplay_inputx form-group has-feedback','id':'#single_cal1','placeholder':_('Start Date')}))
    EndDate = forms.DateField(initial=datetime.date.today,widget=forms.TextInput(attrs={'class': 'form-control xdisplay_inputx form-group has-feedback','id':'#single_cal2','placeholder':_('End Date')}))
    Desc = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':_('Project Details')}))
