from functools import wraps
import datetime
from django.utils import timezone
from drchrono.models import Visitor

def update_estimated_start_treatment_timestamps(f):
    @wraps(f)
    def __decorator(*args, **kwargs):
        res = f(*args, **kwargs)
        # get the time range of today in PST (California)
        today = (timezone.now() - datetime.timedelta(hours=8)).date()
        tomorrow = today + datetime.timedelta(1)
        today_start = datetime.datetime.combine(today, datetime.time()) + datetime.timedelta(hours=8)
        today_end = datetime.datetime.combine(tomorrow, datetime.time()) + datetime.timedelta(hours=8)
        try:
            visitors_in_queue = Visitor.objects.filter(is_active=True, is_queue=True).order_by('create_timestamp')
        except:
            visitors_in_queue = None
        try:
            visitors_with_appointments_today = Visitor.objects.filter(is_active=True, is_confirmed=True,
                                                                      is_appointment=True,
                                                                      estimated_start_timestamp__lte=today_end,
                                                                      estimated_start_timestamp__gte=today_start)
        except:
            visitors_with_appointments_today = None

        print "get queue objs ok"
        print visitors_in_queue
        time_slots_of_appointments = []
        if visitors_with_appointments_today is not None:
            for appointment in visitors_with_appointments_today:
                estimated_start_time = appointment.estimated_start_timestamp
                duration = datetime.timedelta(minutes=appointment.duration)
                time_slots_of_appointments.append([estimated_start_time, estimated_start_time + duration])

        print "check appointment slots ok"
        pre_end_time = timezone.now()
        if visitors_in_queue is not None:
            for visitor in visitors_in_queue:
                # init pre_end_time as the current under treatment patient end time
                if visitor.start_treatment_timestamp is not None:
                    pre_end_time = visitor.estimated_start_timestamp + datetime.timedelta(minutes=visitor.duration)

            for visitor in visitors_in_queue:
                if visitor.start_treatment_timestamp is None:
                    index = find_index_not_match_appointment(pre_end_time,
                                                             pre_end_time + datetime.timedelta(
                                                                 minutes=visitor.duration),
                                                             time_slots_of_appointments)
                    while index != -1:
                        pre_end_time = time_slots_of_appointments[index][1]
                        index = find_index_not_match_appointment(pre_end_time, pre_end_time + datetime.timedelta(
                            minutes=visitor.duration), time_slots_of_appointments)
                    visitor.estimated_start_timestamp = pre_end_time
                    print 'pre visitor save ok'
                    visitor.save()
                    pre_end_time = visitor.estimated_start_timestamp + datetime.timedelta(minutes=visitor.duration)

        print "update queue ok"
        return res
    return __decorator


# helper of updateEstimatedTimestampToStartTreatment()
def find_index_not_match_appointment(starttime, endtime, slots):
    for i in range(0, len(slots)):
        slot = slots[i]
        if not (endtime <= slot[0] or starttime >= slot[1]):
            return i
    return -1


@update_estimated_start_treatment_timestamps
def update_estimation_on_current_aspect():
    return True