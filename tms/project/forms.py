from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

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
    TaskType = forms.CharField(label=_("Task type"),
               widget=forms.TextInput({'class': 'form-control','placeholder':'task'}))
    Duration = forms.IntegerField(label=_("Duration"),
               widget=forms.TextInput({'class': 'form-control','placeholder':'task1'}))
