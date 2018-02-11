import requests
from social_oauth.utils import get_latest_oauth_token

def add_new_patient(data):
    tokenObj = get_latest_oauth_token()

    doctorData = get_doctor_information()
    data['doctor'] = doctorData['doctor']

    headers = {
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    }

    url = 'https://drchrono.com/api/patients'

    r = requests.post(url, data=data, headers=headers)
    print r.json()

    if r.status_code == 201:  # HTTP 201 CREATED
        return {'success': 'OK',
                'patient_id': r.json()['id']}
    return {'error': 'create new appointment failed',
            'response_data': r.json()}


def delete_patient(patient_id):
    tokenObj = get_latest_oauth_token()
    headers = {
        # 'Content-Type':'multipart/form-data',
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    }
    url = 'https://drchrono.com/api/patients/%s'%patient_id
    r = requests.delete(url, headers=headers)

    if r.status_code == 204:  # HTTP 204 DELETE success
        return {'success': 'appointment delete success!',
                'patient_id': patient_id}
    return {'error': 'delete appointment failed',
            'patient_id': patient_id}



def get_current_patient(request):
    email = request.user.email
    print email
    tokenObj = get_latest_oauth_token()
    headers = {
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    }
    # print "headers safe"

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers, params={'email': email}).json()
        patients.extend(data['results'])
        patients_url = data['next']  # A JSON null on the last page
    if len(patients) == 0:
        return None
    return patients[0]


def get_doctor_information():
    tokenObj = get_latest_oauth_token()
    response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    })
    response.raise_for_status()
    data = response.json()
    return data


# @update_estimated_start_treatment_timestamps
def make_new_appointment(data):
    requiredFields = ['doctor', 'duration', 'exam_room', 'office', 'patient', 'scheduled_time']
    for field in requiredFields:
        if field not in data:
            return {'error': 'required field: %s' % field}
    tokenObj = get_latest_oauth_token()
    headers = {
        # 'Content-Type':'multipart/form-data',
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    }
    url = 'https://drchrono.com/api/appointments'
    r = requests.post(url, data=data, headers=headers)

    if r.status_code == 201:  # HTTP 201 CREATED
        return {'success': 'OK',
                'appointment_id': r.json()['id']}
    return {'error': 'create new appointment failed',
            'response_data': r.json()}


def delete_appointment(appointment_id):
    tokenObj = get_latest_oauth_token()
    headers = {
        # 'Content-Type':'multipart/form-data',
        'Authorization': 'Bearer %s' % tokenObj.access_token,
    }
    url = 'https://drchrono.com/api/appointments/%s'%appointment_id
    r = requests.delete(url, headers=headers)

    if r.status_code == 204:  # HTTP 204 DELETE success
        return {'success': 'appointment delete success!',
                'appointment_id': appointment_id}
    return {'error': 'delete appointment failed',
            'appointment_id': appointment_id}


