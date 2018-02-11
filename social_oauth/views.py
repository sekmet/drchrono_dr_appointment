import datetime, requests
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from drchrono.settings import LOGIN_REDIRECT_URL, SOCIAL_AUTH_DRCHRONO_KEY, SOCIAL_AUTH_DRCHRONO_SECRET
from social_oauth.models import OauthToken
from social_oauth.utils import get_latest_oauth_token, refresh_latest_token

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def oauth_page(request):
    if request.method=='POST':
        refresh_latest_token()
        return redirect('home')
    # get new token when request.GET has code param
    if request.GET.get('code',None) is None:
        object = get_latest_oauth_token()
        if object is None:
            context = {'isOauthed': False}
        else:
            context = {'isOauthed': True}
            if object.expires_timestamp < timezone.now()+ datetime.timedelta(seconds=60*60*24):
                if not refresh_latest_token():
                    context['isOauthed']=False
        return render(request, "auth/oauth.html",context)
    else:
        code = request.GET['code']
        # print "code: "+str(code)
        response = requests.post('https://drchrono.com/o/token/', data={
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri':  LOGIN_REDIRECT_URL,
            'client_id': SOCIAL_AUTH_DRCHRONO_KEY,
            'client_secret': SOCIAL_AUTH_DRCHRONO_SECRET,
        })
        response.raise_for_status()

        data = response.json()
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        expires_timestamp = timezone.now() + datetime.timedelta(seconds=data['expires_in'])
        instance = OauthToken.create(access_token,refresh_token,expires_timestamp)
        instance.save()
        context = {'isOauthed': True}
        return render(request, "auth/oauth.html", context)

