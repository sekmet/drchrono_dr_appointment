from django.db import models

# Create your models here.
class OauthToken(models.Model):
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_timestamp =  models.DateTimeField(auto_now_add=False)

    @classmethod
    def create(cls, access_token, refresh_token, expires_timestamp):
        oauthToken = cls(access_token=access_token,refresh_token=refresh_token,expires_timestamp=expires_timestamp)
        return oauthToken

