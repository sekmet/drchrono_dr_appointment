from django.db import models
from django.utils import timezone

# Create your models here.
class Visitor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    create_timestamp = models.DateTimeField(auto_now_add=False)
    estimated_start_timestamp = models.DateTimeField(null=True, blank=True)
    start_treatment_timestamp = models.DateTimeField(null=True, blank=True)
    finish_treatment_timestamp = models.DateTimeField(null=True, blank=True)
    sympton = models.CharField(max_length=1000, default='')
    # visit_date = models.DateField(auto_now_add=True)
    is_appointment = models.BooleanField(default=False)
    is_queue = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=True)
    duration = models.IntegerField(default=30)
    drchrono_appointment_page = models.CharField(max_length=200, default='')
    appointment_data = models.CharField(max_length=600,null=True)
    is_active        = models.BooleanField(default=True)

    @classmethod
    def create(cls, name, email, sympton, duration, appointment_data, drchrono_appointment_page='',is_appointment=False, is_queue=False, is_confirmed=True):
        visitor = cls(name=name, email = email, create_timestamp = timezone.now(),estimated_start_timestamp=None, start_treatment_timestamp=None, finish_treatment_timestamp=None, sympton=sympton, is_appointment=is_appointment, is_queue=is_queue, is_confirmed=is_confirmed,
                      duration=duration, drchrono_appointment_page=drchrono_appointment_page,
                      appointment_data=appointment_data, is_active=True
                      )
        print 'visitor created'
        return visitor
