from django.db import models
import uuid
from datetime import datetime, date
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50)


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    secret = models.UUIDField(default=uuid.uuid4)
    users = models.ManyToManyField(User, related_name='share_groups', through="GroupMember")

    @property
    def num_members(self):
        return len(self.users.all())

    def num_finished(self, wordle):
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

    def get_colors(self):
        colors = ""
        guesses = self.guesses.ljust(30)
        for word_idx in range(6):
            word = self.wordle.answer
            word_colors = ["W", "W", "W", "W", "W"]
            guess = guesses[word_idx*5:(word_idx*5)+5]
            for letter_idx in range(5):
                if(guess[letter_idx] == self.wordle.answer[letter_idx]):
                    word_colors[letter_idx] = "G"
                    word = word.replace(guess[letter_idx], "", 1)
            for letter_idx in range(5):
                if(guess[letter_idx] in word):
                    word_colors[letter_idx] = "Y"
                    word = word.replace(guess[letter_idx], "", 1)
                elif(guess[letter_idx] != " " and word_colors[letter_idx] != "G"):
                    word_colors[letter_idx] = "B"
            colors = colors + "".join(word_colors)
        return colors

    def __str__(self):
        return f"{self.user.username} : Day {self.wordle.day} : {self.guesses}"
