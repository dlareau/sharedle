from django.db import models
from django.contrib.auth.models import User


class Wordle(models.Model):
    answer = models.CharField(max_length=6)
    day = models.IntegerField()


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guesses = models.CharField(max_length=40)
    submission_time = models.DateTimeField()
