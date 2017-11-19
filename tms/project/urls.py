from django.conf.urls import url ,include
from project import views

#application namespace
app_name = 'project'

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^add-sheet/$', views.AddSheet, name='add-sheet'),
    url(r'^add_project/$', views.AddProject, name='add-project'),
    url(r'^my_sheet/$', views.MySheet, name='my-sheet'),
    url(r'^dept_sheet/$', views.DeptSheet, name='dept-sheet'),
]
