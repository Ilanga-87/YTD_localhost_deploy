from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import YouTubeURLForm

# Create your views here.


def index(request):
    return render(request, 'audio/index.html')


def get_link(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('get_link')
    else:
        form = YouTubeURLForm()
    return render(request, 'audio/index.html', {'form': form})

