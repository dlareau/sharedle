from django.db import models
import uuid
from django.contrib.auth.models import User


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    players = models.ManyToManyField(Player, related_name='groups', through="GroupMember")


class GroupMember(models.Model):
    nickname = models.CharField(max_length=200)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Wordle(models.Model):
    answer = models.CharField(max_length=6)
    day = models.IntegerField()


class Submission(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    wordle = models.ForeignKey(Wordle, on_delete=models.CASCADE)
    guesses = models.CharField(max_length=40)
    submission_time = models.DateTimeField()
