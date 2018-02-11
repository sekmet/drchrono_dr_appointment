from django.contrib import admin

# Register your models here.

from social_oauth.models import OauthToken


class OauthAdmin(admin.ModelAdmin):
    # list_display = ['__str__', 'slug']
    class Meta:
        model = OauthToken


admin.site.register(OauthToken, OauthAdmin)
