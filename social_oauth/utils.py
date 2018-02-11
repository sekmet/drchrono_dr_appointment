import datetime, requests
from django.utils import timezone
from drchrono.settings import SOCIAL_AUTH_DRCHRONO_SECRET, SOCIAL_AUTH_DRCHRONO_KEY
from social_oauth.models import OauthToken


def get_latest_oauth_token():
    try:
        object = OauthToken.objects.latest("expires_timestamp")
        if object.expires_timestamp < timezone.now():
            object = None
    except OauthToken.DoesNotExist:
        object = None

    return object


def refresh_latest_token():
    object = get_latest_oauth_token()
    if object is None:
        return False
    response = requests.post('https://drchrono.com/o/token/', data={
        'refresh_token': object.refresh_token,
        'grant_type': 'refresh_token',
        'client_id': SOCIAL_AUTH_DRCHRONO_KEY,
        'client_secret': SOCIAL_AUTH_DRCHRONO_SECRET,
    })
    response.raise_for_status()
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = timezone.now() + datetime.timedelta(seconds=data['expires_in'])
    instance = OauthToken.create(access_token, refresh_token, expires_timestamp)
    instance.save()
    return True

