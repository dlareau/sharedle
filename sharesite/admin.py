from django.contrib import admin
from django.contrib.auth.models import User
from . import models

admin.site.register(models.Wordle)
admin.site.register(models.Submission)
admin.site.register(models.Group)
admin.site.register(models.GroupMember)
