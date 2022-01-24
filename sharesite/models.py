from django.db import models
import uuid
from datetime import datetime, date
from django.utils import timezone
from django.contrib.auth.models import User


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.UUIDField(default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name='share_groups', through="GroupMember")

    @property
    def num_members(self):
        return len(self.users.all())

    @property
    def num_finished(self):
        wordle = Wordle.get_current_wordle()
        submissions = Submission.objects.filter(wordle=wordle, user__share_groups__id=self.id)
        return len(submissions)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='one_group')
        ]

    nickname = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname


class Wordle(models.Model):
    answer = models.CharField(max_length=6)
    day = models.IntegerField()

    @classmethod
    def get_current_wordle(cls):
        print(timezone.localtime())
        print(timezone.localtime().date())
        day = (timezone.localtime().date() - date(2021, 6, 19)).days
        print(day)
        return cls.objects.get(day=day)


    def __str__(self):
        return f"Day {self.day}: {self.answer}"


class Submission(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'wordle'], name='one_wordle')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wordle = models.ForeignKey(Wordle, on_delete=models.CASCADE)
    guesses = models.CharField(max_length=40)
    submission_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} : Day {self.wordle.day} : {self.guesses}"
