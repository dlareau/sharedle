from django.db import models
import uuid
import re
from datetime import datetime, date
from django.contrib.auth.models import User
from pathlib import Path

from .utils import chunks

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=50)
    high_contrast = models.BooleanField(default=False)


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
        return f"{self.nickname} => {self.group.name}" 


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
    statistics_data = models.JSONField(blank=True, null=True)

    @property
    def statistics(self):
        if(self.statistics_data is None):
            # last_guess_chance
            words = []
            guesses = self.guesses[:-5]
            guessed_words = chunks(self.guesses, 5)
            with open(Path(__file__).resolve().parent / "static/sharesite/words.js", "r") as f:
                words = f.read()[21:-8].replace('"', '').strip().split(", ")#[:2315]
                words = [word.upper() for word in words]
            found_bad_letters = list(set([l for l in guesses if l not in self.wordle.answer]))
            found_good_letters = list(set([l for l in guesses if l in self.wordle.answer]))
            colors = self.get_colors()[:len(guesses)]
            matches = list(set([i.start() % 5 for i in re.finditer("G", colors)]))
            regex_str = ""
            for i in range(5):
                if(i in matches):
                    regex_str = regex_str + self.wordle.answer[i]
                else:
                    regex_str = regex_str + f"[^{''.join(found_bad_letters)}]"
            regex = re.compile(regex_str)
            possible_words = [word for word in words if regex.match(word)]
            for letter in found_good_letters:
                possible_words = [word for word in possible_words if letter in word]
            possible_words = [word for word in possible_words if word not in guessed_words]
            # return ", ".join(possible_words)
            return f"1 in {len(possible_words) + 1} chance"

        else:
            return self.statistics_data

    def get_colors(self):
        colors = ""
        guesses = chunks(self.guesses.ljust(30), 5)
        for guess in guesses:
            word = self.wordle.answer
            word_colors = ["W", "W", "W", "W", "W"]
            for letter_idx in range(5):
                if(guess[letter_idx] == self.wordle.answer[letter_idx]):
                    word_colors[letter_idx] = "G"
                    word = word.replace(guess[letter_idx], "", 1)
            for letter_idx in range(5):
                if(word_colors[letter_idx] != "G"):
                    if(guess[letter_idx] in word):
                        word_colors[letter_idx] = "Y"
                        word = word.replace(guess[letter_idx], "", 1)
                    elif(guess[letter_idx] != " "):
                        word_colors[letter_idx] = "B"
            colors = colors + "".join(word_colors)
        return colors

    def __str__(self):
        return f"{self.user.username} : Day {self.wordle.day} : {self.guesses}"
