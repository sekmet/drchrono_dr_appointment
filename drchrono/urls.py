from django.conf.urls import include, url
from django.contrib import admin

from views import hello_world, home_page, login_page, register_page, queue_page, appointments_page, contact_page, \
    logout_page

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    url(r'^admin/', admin.site.urls),
    url(r'^hello/$', hello_world, name='hello'),
    url(r'^$', home_page,name='home'),
    # url(r'^home/$', home_page, name='home'),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$', logout_page, name='logout'),
    url(r'^register/$', register_page, name='register'),
    url(r'^queue/$', queue_page, name='queue'),
    url(r'^appointments/$', appointments_page, name='appointments'),
    # url(r'^make-appointment/$', make_appointment_page, name='make-appointment'),
    url(r'^contact/$', contact_page, name='contact'),

    url(r'', include('social_oauth.urls', namespace='social')),
]
