from django.conf.urls import include, url
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # app/ -> Genetelella UI and resources
    url(r'^project/', include('project.urls')),
    url(r'^', include('project.urls')),

]
