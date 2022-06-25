from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.utils.text import slugify
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView
from django.conf import settings
from django.http import FileResponse

from celery import chord, chain

from .forms import YouTubeURLForm
from .models import Conversion
from .tasks import download, send_link
from .service import extract_single_from_playlist, get_video_id, generate_slug_tail


# Create your views here.

class ConvertView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    template_name = "audio/index.html"
    success_url = "/success-page"

    def form_valid(self, form):
        instance = form.save(commit=False)
        video = extract_single_from_playlist(form.cleaned_data["video_url"])
        user_email = form.cleaned_data["user_email"]
        video_id = get_video_id(video)
        slug_tail = generate_slug_tail(10)
        slug = slugify(f"{video_id}-{slug_tail}")
        instance.video_id = video_id
        instance.slug = slug #TODO exclusive

        possible_previous_conversion = Conversion.objects.filter(video_id=instance.video_id)
        if possible_previous_conversion and Conversion.objects.get(video_id=instance.video_id).audio_file.name != '':
            previous_conversion = Conversion.objects.get(video_id=instance.video_id)
            return redirect(f"/load-audio-{previous_conversion.slug}")

        instance.save()

        link = f"https://my_site.com/{self.success_url}-{slug}"
        (download.si(video, slug) | send_link.si(user_email, link))()

        return redirect(f"{self.success_url}-{slug}")


class MyView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    success_url = "/success-page"
    template_name = "audio/index.html"

    def form_valid(self, form):


        # form.save()
        return redirect(self.success_url)


class SuccessView(TemplateView):
    model = Conversion
    template_name = "audio/get_link.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Wait for download"
        return context


class LoadView(DetailView):
    model = Conversion
    template_name = "audio/load_audio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Get it!"
        return context


def download_audio(request, title):
    audio_file = FileResponse(open(f'uploads/audio/{title}', 'rb'), as_attachment=True)
    return audio_file


class NewView(TemplateView):
    model = Conversion
    template_name = "audio/load_audio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
        return context
