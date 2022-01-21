from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):

    return render(request, "sharesite/index.html", {})
