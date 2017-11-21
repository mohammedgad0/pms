from django.conf.urls import include, url
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from project import views
import project.forms
import project.views
from datetime import datetime
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # app/ -> Genetelella UI and resources
    url(r'^project/', include('project.urls')),
    url(r'^', include('project.urls')),
    url(r'^accounts/login/$',
        views.myuser,
        {
            'template_name': 'project/login.html',
            'authentication_form': project.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),



]
