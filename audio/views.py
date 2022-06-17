from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView

from .forms import YouTubeURLForm
from .models import Conversion
from .tasks import do_mult, download
from .service import extract_single_from_playlist, get_video_id


# Create your views here.

class ConvertView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    template_name = "audio/index.html"
    success_url = "/success-page"

    def form_valid(self, form):
        instance = form.save(commit=False)
        video = extract_single_from_playlist(form.cleaned_data["video_url"])
        slug = get_video_id(video)
        instance.slug = slug

        previous_conversion = Conversion.objects.filter(slug=instance.slug)
        if previous_conversion and Conversion.objects.get(slug=instance.slug).audio_file.name != '':
            return redirect(f"/load-audio-{instance.slug}")

        instance.save()

        download.delay(video, slug)

        return redirect(f"{self.success_url}-{slug}")


class MyView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    success_url = "/success-page"
    template_name = "audio/index.html"

    def form_valid(self, form):
        print(do_mult.delay(8, 4))

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


class NewView(TemplateView):
    model = Conversion
    template_name = "audio/load_audio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN"
        return context
