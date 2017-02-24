from django.contrib import admin
from web import models
# Register your models here.
from web import custom_user_admin


admin.site.register(models.Host)
admin.site.register(models.RemoteUser)
admin.site.register(models.BindHost)
admin.site.register(models.IDC)
admin.site.register(models.HostGroups)
# admin.site.register(models.UserProfile)
admin.site.register(models.SessionRecord)
