
from django.conf.urls import url

from .views import oauth_page

urlpatterns = [

    url(r'^oauth/$', oauth_page, name='oauth'),

]