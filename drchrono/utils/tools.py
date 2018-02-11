import datetime
import random
from drchrono.models import Visitor

# format : '2018-02-08T23:58', return string
def transform_PST_str_to_UTC_str(pst_datetime):
    pst_timestamp = datetime.datetime.strptime(pst_datetime, '%Y-%m-%dT%H:%M')
    pst_timestamp = pst_timestamp + datetime.timedelta(hours=8)
    return pst_timestamp.strftime('%Y-%m-%dT%H:%M')


# TODO: logic to estimate visiting duration of each request.
# currently use a random number
def get_estimated_visiting_duration(request, default=30):
    sympton = request.session.get('sympton', '')
    try:
        previous_visits = Visitor.objects.filter(email=request.user.email)
    except:
        previous_visits = None
    if previous_visits is None:
        return default
    else:
        return random.randint(10, 40)
