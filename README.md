# drchrono Hackathon: Dr-appointment

## Description
Many clinics provide walk-in services. However, patients typically have no idea about how long the waiting queue is until they arrive at the clinics. It will be beneficial to both patients and doctors if the visitors know the estimated waiting time before they stop by.

By providing an online queue and appointment system, this project is built for solving this problem. Besides functionalities like making appointments, joining the queue, and manage treatment sessions, this system brings the following extra benefits:
- Patients could join queue online, instead of coming to office in-person.
- Patients could see the queue length, the estimated waiting time in real-time.
- The estimated treatment duration is decided by an algorithm which is based on the history and symptoms of the patient, instead of doctor's estimation.
- Doctors could send an email notification when picking up persons in the queue.
- The system is closely integrated with Drchrono fully featured EHR system: FHIR platform.


## Requirements
- [pip](https://pip.pypa.io/en/stable/)
- [python virtual env](https://packaging.python.org/installing/#creating-and-using-virtual-environments)

## Setup
First, setup the configuration of `oauth` and `send email` by setting the fields in `drchrono/settings.py` file:
```
# authentication settings
SOCIAL_AUTH_DRCHRONO_KEY
SOCIAL_AUTH_DRCHRONO_SECRET
LOGIN_REDIRECT_URL
LOGIN_URL
SOCIAL_AUTH_DRCHRONO_SCOPE

# email setting
DEFAULT_FROM_EMAIL
EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_PORT
EMAIL_USE_TLS
```

Then, run the following commands:
``` bash
$ pip install -r requirements.txt
$ python manage.py runserver
```
## Screenshots of the system

#### Anonymous user
home page:
![anonymous_home](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/anonymous/home.PNG)  

login page:
![anonymous_login](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/anonymous/login.PNG)

register page: all registrations are stored in Drchrono
![anonymous_register](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/anonymous/register.PNG)  

#### Patient
home page: according to patient's status, he/she could see information like `queue length`, `waiting time in the queue`, and `appointment waiting time`.
![patients_home](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/patients/homePNG.PNG)  

#### Doctor
queue page: `Yellow` card represents patient under treatment, `blue` card represents patients in the queue, `green` card represents appointment. Doctor can do actions including `sending email notification`, `start treatment`, `go to Drchrono appointment page`, `move patient to the next position of the queue`, `cancel treatment`, and `finish treatment`.
![doctor_queue](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/doctors/queue.PNG)  

appointment requests page: `confirm` means making an appointment in Drchrono. `Reject` means delete this appointment info from local database.
![appointment_requests](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/doctors/appointment_requests.PNG) 

oauth page: `authenticate` tag can be seen when `this app` is not authenticated from Drchrono. `refresh auth token` can refresh authentication from Drchrono.
![oauth](https://github.com/xujingyapatrick/drchrono_dr_appointment/blob/master/figures/doctors/oauth.PNG) 



