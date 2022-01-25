from datetime import datetime, date
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import Group, GroupMember, Submission, Wordle


# Create your views here.
def index(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if("next" in request.POST and request.POST.get("next") != ""):
                return redirect(request.POST.get('next'))
    else:
        form = UserCreationForm()
    return render(request, "sharesite/index.html", {"form": form})


def login_async(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"result": "success"})
        else:
            return JsonResponse({"result": "fail"})
    return JsonResponse({"result": "invalid request"})


@login_required
def update_profile(request):
    if request.method == "POST":
        if "timezone" in request.POST:
            request.user.profile.timezone = request.POST.get("timezone")
            request.user.profile.save()
            return JsonResponse({"result": "success"})
    return JsonResponse({"result": "invalid request"})

@login_required
def input(request):
    wordle = Wordle.get_current_wordle(request.user)
    if request.method == "POST":
        if "grid" in request.POST:
            grid = request.POST.get('grid')
            Submission.objects.create(user=request.user, wordle=wordle,
                                      guesses=grid, submission_time=datetime.now())
        elif "operation" in request.POST and request.POST.get("operation") == "clear":
            submission = Submission.objects.get(user=request.user, wordle=wordle).delete()
    try:
        submission = Submission.objects.get(user=request.user, wordle=wordle)
        grid = submission.guesses
    except Submission.DoesNotExist:
        grid = ""

    return render(request, "sharesite/input.html", {"grid": grid, "correct_word": wordle.answer})


@login_required
def groups(request):
    if request.method == "POST" and "name" in request.POST:
        name = request.POST.get("name")
        group = Group.objects.create(name=name, owner=request.user)
        GroupMember.objects.create(group=group, user=request.user, nickname=request.user.username)
    if("all" in request.GET and request.user.is_superuser):
        groups = Group.objects.all()
    else:
        groups = request.user.share_groups.all()
    wordle = Wordle.get_current_wordle(request.user)
    for group in groups:
        group.num_finished_curr = group.num_finished(wordle)
    return render(request, "sharesite/groups.html", {"groups": groups})


@login_required
def invite(request, group_id, secret):
    group = Group.objects.get(id=group_id)
    if(group.secret == secret):
        try:
            GroupMember.objects.create(group=group, user=request.user, nickname=request.user.username)
        except IntegrityError:
            pass
    return groups(request)


@login_required
def group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST" and "action" in request.POST and request.user == group.owner:
        action = request.POST.get("action")
        if(action == "rename"):
            group.name = request.POST.get("name")
            group.save()
        elif(action == "remove"):
            GroupMember.objects.get(pk=request.POST.get("user")).delete()
        elif(action == "delete"):
            group.delete()
            return redirect("/groups/")

    wordle = Wordle.get_current_wordle(request.user)
    if("all" in request.GET and request.user.is_superuser):
        members = User.objects.all()
        done = True
    else:
        members = GroupMember.objects.filter(group=group).order_by(Lower('nickname'))
        done = Submission.objects.filter(user=request.user, wordle=wordle).count() == 1
    data = []
    for member in members:
        try:
            submission = Submission.objects.get(user=member.user, wordle=wordle)
            guess = submission.guesses.ljust(30)
            colors = submission.get_colors()
            if(not done):
                guess = " " * 30
            grid = list(zip(guess, colors))
        except Submission.DoesNotExist:
            grid = list(zip(" " * 30, "W" * 30))
        data.append({"name": member.nickname, "pk": member.pk, "grid": grid})
    return render(request, "sharesite/group.html", {"wordle": wordle, "player_data": data, "group": group, "domain": settings.DOMAIN})
