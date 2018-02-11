from django.contrib import admin

# Register your models here.
from django.contrib.sessions.models import Session

from drchrono.models import Visitor


class SessionAdmin(admin.ModelAdmin):
    class Meta:
        model = Session
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']

class VisitorAdmin(admin.ModelAdmin):
    class Meta:
        model = Visitor
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['email', 'sympton', 'is_appointment', 'is_queue', 'is_confirmed']


admin.site.register(Session, SessionAdmin)
admin.site.register(Visitor, VisitorAdmin)
