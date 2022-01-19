from django.contrib import admin
from django.contrib.auth.models import User
from . import models


class UserProxyObject(User):
    class Meta:
        proxy = True
        app_label = 'sharesite'
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural
        ordering = ['-pk']


class UserProxyAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    search_fields = ['email', 'username', 'first_name', 'last_name']


admin.site.register(models.Wordle)
admin.site.register(models.Submission)
admin.site.register(UserProxyObject, UserProxyAdmin)
