from django.conf.urls import url
from .apiviews import add_phase

app_name = 'api'


urlpatterns = [
    url(r'add_phase', add_phase, name='add_phase'),
]
