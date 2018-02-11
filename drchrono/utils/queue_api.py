import ast
import datetime
from django.core.mail import send_mail
from django.utils import timezone

from drchrono.models import Visitor
from drchrono.settings import DEFAULT_FROM_EMAIL

from drchrono.utils.drchrono_api import make_new_appointment, get_doctor_information, delete_appointment


def perform_actions_on_visitor(data):
    # cancel_treatment, start_treatment,finish_treatment, move_to_next
    if 'action' not in data or 'id' not in data:
        return {'error': "data form error"}
    try:
        visitor = Visitor.objects.filter(id=data.get('id')).first()
        if data.get('action') == 'start_treatment':
            if visitor.is_queue:
                data = ast.literal_eval(visitor.appointment_data)
                data['scheduled_time'] = timezone.now()
                # change UTC to PST for drchrono
                data['scheduled_time'] = data['scheduled_time'] -datetime.timedelta(hours=8)

                # doctor can not pick a queued person when there is only 1 minits before an appointment
                data['duration'] = 1
                r = make_new_appointment(data)
                if 'success' in r:
                    try:
                        # https: // xujingyastan.drchrono.com / appointments / 76232954 /
                        url = "https://%s.drchrono.com/appointments/%s/" % (
                            get_doctor_information().get('username'), r.get('appointment_id', 'id_required'))
                        visitor.drchrono_appointment_page = url
                        visitor.start_treatment_timestamp = timezone.now()
                        visitor.estimated_start_timestamp= timezone.now()
                        visitor.save()
                    except:
                        print 'visitor start_treatment fail'
                        r = delete_appointment(r.get('appointment_id', 'id_required'))
                        print r

                return r
            if visitor.is_appointment:
                visitor.start_treatment_timestamp = timezone.now()
                visitor.save()
                return {'success': 'OK'}
            return {'error': 'visitor type error'}

        if data.get('action') == 'finish_treatment':
            visitor.finish_treatment_timestamp = timezone.now()
            visitor.is_active = False
            visitor.save()
            return {'success': 'OK'}

        if data.get('action') == 'cancel_treatment':
            url = visitor.drchrono_appointment_page
            if url.startswith('http'):
                parts = url.split('/')
                appointment_id = parts[-2]
                r = delete_appointment(appointment_id)
                print r

            visitor.is_active = False
            visitor.save()
            return {'success': 'OK'}

        if data.get('action') == 'move_to_next':
            try:
                nextVisitor = Visitor.objects.filter(is_active=True, is_queue=True,
                                                     create_timestamp__gt=visitor.create_timestamp).order_by(
                    'create_timestamp').first()
                tmpCreatedTimeStamp = visitor.create_timestamp
                visitor.create_timestamp = nextVisitor.create_timestamp
                visitor.save()
                nextVisitor.create_timestamp = tmpCreatedTimeStamp
                nextVisitor.save()
            except Exception as e:
                print e
            return {'success': 'OK'}

        if data.get('action') == 'send_email_notification':
            try:
                send_mail(
                    'Dr-appointment notification: Time To Start Treatment',
                    "Hello: %s: \n     It is your turn to see doctor. Please come to office, doctor is waiting for you"%visitor.name,
                    DEFAULT_FROM_EMAIL,
                    [visitor.email],
                    fail_silently=False,
                )
                return {'success': 'email sent!'}
            except Exception as e:
                print e
                return {'error': 'sending mail to %s, with email as: %s failed'%(visitor.name, visitor.email) }
    except:
        return {'error': "visitor with id = %s can not be found" % data.get('id')}



# helper of updateEstimatedTimestampToStartTreatment()
def find_index_not_match_appointment(starttime, endtime, slots):
    for i in range(0, len(slots)):
        slot = slots[i]
        if not (endtime <= slot[0] or starttime >= slot[1]):
            print i
            return i
    print 'find_index_not_match_appointment end'
    return -1


def get_queue_tail_timestamp():
    try:
        visitor = Visitor.objects.filter(is_active=True, is_queue=True).order_by('estimated_start_timestamp').last()
    except:
        visitor = None

    if visitor is None:
        return timezone.now()
    else:
        return visitor.estimated_start_timestamp + datetime.timedelta(minutes=visitor.duration)


def get_queue_user_estimated_start_time(request):
    if request.user.is_superuser or not request.user.is_authenticated:
        print 'visitor not allowed to join queue'
        return None

    try:
        visitor = Visitor.objects.filter(email=request.user.email, is_active=True, is_queue=True).order_by(
            'estimated_start_timestamp').first()
        print 'visitor found!!'
        return visitor.estimated_start_timestamp
    except:
        print 'no visitor found!!'
        return None


def get_appointment_user_scheduled_time(request):
    if request.user.is_superuser or not request.user.is_authenticated:
        print 'visitor not allowed to make appointment'
        return None

    try:
        visitor = Visitor.objects.filter(email=request.user.email, is_active=True, is_appointment=True,
                                         is_confirmed=True).order_by(
            'estimated_start_timestamp').first()
        return visitor.estimated_start_timestamp
    except:
        return None

