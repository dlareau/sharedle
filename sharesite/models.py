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
    show_statistics = models.BooleanField(default=False)


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

    def statistics(self, regenerate=False):
        if(self.statistics_data is None or regenerate):
            #### last_guess_chance ####

            # divide up guesses
            guesses = self.guesses[:-5]
            guessed_words = chunks(self.guesses, 5)
            colors = chunks(self.get_colors()[:len(guesses)], 5)

            # get words: todo save this for speed
            words = []
            with open(Path(__file__).resolve().parent / "static/sharesite/words.js", "r") as f:
                words = f.read()[21:-8].replace('"', '').strip().split(", ")#[:2315]
                words = [word.upper() for word in words]

            found_bad_letters = []
            found_good_letters = []
            matches = []
            num_left = [len(words)]
            for guess, coloring in zip(guessed_words, colors):
                if guess in words:
                    words.remove(guess)
                found_bad_letters = list(set(found_bad_letters + [l for l in guess if l not in self.wordle.answer]))
                found_good_letters = list(set(found_good_letters + [l for l in guess if l in self.wordle.answer]))
                matches = list(set(matches + [i.start() for i in re.finditer("G", coloring)]))
                regex_str = ""
                for i in range(5):
                    if(i in matches):
                        regex_str = regex_str + self.wordle.answer[i]
                    else:
                        regex_str = regex_str + f"[^{''.join(found_bad_letters)}]"
                regex = re.compile(regex_str)
                words = [word for word in words if regex.match(word)]
                for letter in found_good_letters:
                    words = [word for word in words if letter in word]
                num_left.append(len(words))
            num_left.append(1)
            num_left = num_left + ([1] * (7 - len(num_left)))
            self.statistics_data = num_left
            self.save()
            return num_left

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
