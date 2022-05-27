from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import YouTubeURLForm
import youtube_dl

# Create your views here.


def index(request):
    return render(request, 'audio/index.html')


def get_link(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Great!')
            return HttpResponseRedirect('get_link')
    else:
        form = YouTubeURLForm()
    return render(request, 'audio/index.html', {'form': form})


def my_func(request):
    return render(request, 'audio/get_link.html')

