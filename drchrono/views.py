# Create your views here.
import ast, datetime, pytz
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView

from drchrono.forms import LoginForm, RegisterForm, AppointmentForm, JoinQueueForm
from drchrono.models import Visitor
from drchrono.settings import TIME_ZONE
from drchrono.decorators import update_estimated_start_treatment_timestamps, update_estimation_on_current_aspect
from drchrono.utils.drchrono_api import get_doctor_information, add_new_patient, delete_patient, get_current_patient, \
    make_new_appointment, delete_appointment
from drchrono.utils.queue_api import get_queue_tail_timestamp, get_queue_user_estimated_start_time, \
    get_appointment_user_scheduled_time, perform_actions_on_visitor
from drchrono.utils.tools import get_estimated_visiting_duration, transform_PST_str_to_UTC_str


def hello_world(request):
    context = {}
    return render(request, "helloworld.html", context)


def home_page(request):
    # print "userdata"
    # print(request.session.get('userdata', 'no user logged in'))
    print request.user
    print "authenticated: %s" % str(request.user.is_authenticated())
    print "superuser: %s" % str(request.user.is_superuser)
    r = get_doctor_information()
    print r

    context = {'page_name': "home",
               'queue_form': JoinQueueForm(),
               'appointment_form': AppointmentForm(),
               'queue_tail': get_queue_tail_timestamp(),
               'queue_user_start_timestamp': get_queue_user_estimated_start_time(request),
               'appointment_scheduled_timestamp': get_appointment_user_scheduled_time(request)
               }
    print context

    return render(request, "home.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        # check if the user is in the database
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("/")
        return redirect('/register/')

    return render(request, "auth/login.html", context)


def logout_page(request):
    auth.logout(request)

    context = {'page_name': "home"}
    return redirect('home')


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        data = form.cleaned_data
        r = add_new_patient(data)

        if 'success' in r:
            try:
                User.objects.create_user(data['email'], data['email'], data['password'])
                user = authenticate(username=data['email'], password=data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('/')
            except:
                r_del = delete_patient(r.get('patient_id', ''))
                return JsonResponse(r_del)

    context['page_name'] = "register"
    return render(request, "auth/register.html", context)


class VisitorQueueListView(ListView):
    def get_queryset(self):
        request = self.request
        queryset = []
        try:
            # get the time range of today in PST (California)
            today = (timezone.now() - datetime.timedelta(hours=8)).date()
            tomorrow = today + datetime.timedelta(1)
            today_start = datetime.datetime.combine(today, datetime.time()) + datetime.timedelta(hours=8)
            today_end = datetime.datetime.combine(tomorrow, datetime.time()) + datetime.timedelta(hours=8)
            print 'now: %s' % str(timezone.now())
            print 'today_start: %s' % str(today_start)
            print 'today_end: %s' % str(today_end)
            queryset = Visitor.objects.filter(Q(is_active=True),
                                              Q(is_queue=True) | Q(is_appointment=True, is_confirmed=True,
                                                                   estimated_start_timestamp__lte=today_end,
                                                                   estimated_start_timestamp__gte=today_start)).order_by(
                'estimated_start_timestamp')

            return queryset
        except:
            return queryset

    template_name = "manager/queue.html"


@login_required
@update_estimated_start_treatment_timestamps
def queue_page(request):
    if request.method == 'GET' and request.user.is_superuser:
        return VisitorQueueListView.as_view()(request)

    if request.method == 'POST' and request.user.is_superuser:
        data = request.POST
        r = perform_actions_on_visitor(data)
        if 'success' not in r:
            return JsonResponse(r)
        return redirect('queue')

    # create queue or appointment visitor
    if request.method == 'POST' and request.is_ajax():
        print "is_ajax    aaa"
        patient = get_current_patient(request)

        data = {'doctor': get_doctor_information().get('doctor'),
                'duration': get_estimated_visiting_duration(request),
                # use default exam_room and office
                'exam_room': 2,
                'office': 214564,
                'patient': patient.get('id')}
        # print data

        formData = request.POST
        request.session['sympton'] = formData.get('sympton', '')

        # datetime transform
        if formData.get('appointmentType') is not None and formData.get('appointmentType') == 'appointment':
            data['scheduled_time'] = formData.get('time-to-visit', None)
            # utc_time = transform_PST_str_to_UTC_str(formData.get('time-to-visit',None))
            # data['scheduled_time'] = utc_time

        print formData
        # name, sympton, duration, appointment_data, drchrono_appointment_page='',is_appointment=False, is_queue=False, is_confirmed=True
        visitor = Visitor.create(
            name="%s %s" % (patient.get('first_name', 'unknown'), patient.get('last_name', '')),
            email=patient.get('email', 'unknown'),
            sympton=formData.get('sympton', ''),
            duration=data.get('duration'),
            is_appointment=(formData.get('appointmentType') == 'appointment'),
            is_queue=(formData.get('appointmentType') == 'queue'),
            is_confirmed=(formData.get('appointmentType') != 'appointment'),
            drchrono_appointment_page='',
            appointment_data=data
        )

        print visitor
        print visitor.sympton
        print visitor.name
        try:
            visitor.save()
        except Exception as e:
            return JsonResponse({'error': 'creation error: %s' % str(e)}, status=400)
        print "ajax finished"

        # update queue estiamtion times when create new queue visitor
        # update = [update_estimation_on_new_queue_member_created]

        return JsonResponse({'result': 'success'}, status=201)
    else:
        return JsonResponse({'error': 'bad request'}, status=400)


class AppointmentRequestListView(ListView):
    queryset = Visitor.objects.all().filter(is_confirmed=False, is_active=True)
    template_name = "manager/appointments.html"


@user_passes_test(lambda u: u.is_superuser)
def appointments_page(request):
    if request.method == 'GET':
        print "GET appointments"
        return AppointmentRequestListView.as_view()(request)
    elif request.method == 'POST':
        formData = request.POST
        if formData is None:
            return JsonResponse({'error': 'no data in POST'}, status=400)
        try:
            print formData
            visitor = Visitor.objects.filter(id=int(formData.get('id', ''))).first()
            print visitor
            if formData.get('action', '') == 'confirm-of-appointment':
                print visitor.appointment_data
                # print type(visitor.appointment_data)
                data = ast.literal_eval(visitor.appointment_data)
                print data
                print data['scheduled_time']
                print type(data['scheduled_time'])

                r = make_new_appointment(data)
                print r
                if 'success' in r:
                    try:
                        visitor.is_confirmed = True
                        # https: // xujingyastan.drchrono.com / appointments / 76232954 /
                        url = "https://%s.drchrono.com/appointments/%s/" % (
                            get_doctor_information().get('username'), r.get('appointment_id', 'id_required'))
                        visitor.drchrono_appointment_page = url
                        # 2018-02-10T09:00
                        estimated_start_timestamp = transform_PST_str_to_UTC_str(data['scheduled_time'])
                        estimated_start_timestamp = datetime.datetime.strptime(estimated_start_timestamp,
                                                                               '%Y-%m-%dT%H:%M')
                        estimated_start_timestamp = estimated_start_timestamp.replace(tzinfo=pytz.timezone(TIME_ZONE))
                        print estimated_start_timestamp

                        visitor.estimated_start_timestamp = estimated_start_timestamp
                        visitor.save()
                        update_estimation_on_current_aspect()
                        return redirect('appointments')
                    except:
                        print 'confirm appointment failed'
                        r_del = delete_appointment(r.get('appointment_id', 'id_required'))
                        print r_del
                else:
                    return JsonResponse(r)
            elif formData.get('action', '') == 'reject':
                visitor.is_active = False
                visitor.save()
                return redirect('appointments')
        except Exception as e:
            print e

            return JsonResponse({'error': 'creating appointment in drchrono failed'}, status=400)
    else:
        return JsonResponse({'error': 'only superuser can make appointments'}, status=403)


def contact_page(request):
    context = {'page_name': "contact"}
    return render(request, "client/contact.html", context)
