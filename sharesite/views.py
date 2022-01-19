from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponse('ok')
    else:
        form = UserCreationForm()

    return render(request, "sharesite/register.html", {'form': form})
