from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
# from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, DetailView

from pytils.translit import slugify as sg

from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from .forms import YouTubeURLForm
from .models import Conversion
from .tasks import do_mult


# Create your views here.


def extract_single_from_playlist(video):
    splitted_url = video.split('&')
    return splitted_url[0]


def get_video_id(video):
    splitted_id = video.split("=")
    return splitted_id[-1]


def download(video):
    ydl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': 'uploads/audio/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video, download=False)
            video_title = video_info.get("title", None)
            slug = get_video_id(video)
            # conversion.title = video_title
            audio = ydl.download([video])
            # conversion.audio_file.name = f"upload/audio/{conversion.title}.mp3"

            # print(f"***********{conversion.title}")
            # print(f"++++++++ AND THIS IS {video_title}")
            print(f"SLUUUUUUUUG {slug}")
    except YoutubeDLError as err:
        print("Something get wrong")
        # TODO return error page
    # через ютдл из урла получить название видео + присвоить его title
    #
    # через дэйт тайм получиь таймстамп + присвоить его pub_time
    return redirect(f"/load-page-{slug}")


class ConvertView(SuccessMessageMixin, CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    template_name = "audio/index.html"
    success_url = "/success-page"

    def get_context_data(self, **kwargs):
        context = super(ConvertView, self).get_context_data(**kwargs)
        context["message"] = "Congratsssss"
        return context

    def form_valid(self, form):
        do_mult.apply_async((3, 7), countdown=10)
        print(do_mult.delay(8, 4))
        messages.success = (self.request, "JJDJJDJEJEJI")
        self.get_context_data()

        instance = form.save(commit=False)
        print(f"***** THIS IS {instance}")
        video = extract_single_from_playlist(form.cleaned_data["video_url"])
        slug = get_video_id(video)
        print(slug)

        conversion = Conversion()
        conversion.slug = slug
        print(conversion.slug)
        conversion.video_url = video

        ytdl_opts = {
            'quiet': True
        }

        with YoutubeDL(ytdl_opts) as ydl:
            video_info = ydl.extract_info(video, download=False)
            video_title = video_info.get("title", None)
            conversion.title = video_title

        # TODO UNLOCK пишем условие. если видео айди есть в базе данных, сразу редирект на страницу скачки. если нет, редирект на саксесс пэйдж
        #     if Conversion.objects.filter(slug=conversion.slug).exists() and conversion.audio_file is not None:
        #         return redirect(f"/load-audio-{conversion.slug}")

        conversion.save()
        return redirect(f"{self.success_url}-{conversion.slug}")


class MyView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    success_url = "/success-page"
    template_name = "audio/index.html"

    def form_valid(self, form):

        print(do_mult.delay(8, 4))

        # form.save()
        return redirect(self.success_url)


class SuccessView(UpdateView):
    model = Conversion
    template_name = "audio/get_link.html"
    success_url = "/new-page"
    fields = ["audio_url", "pub_time", "audio_file"]

    # def get_object(self, queryset=None):
    #     if queryset is None:
    #         queryset = self.get_queryset()
    #
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     if slug is not None:
    #         slug_field = self.get_slug_field()
    #         queryset = queryset.filter(**{slug_field: slug})
    #
    #     try:
    #         obj = queryset.get()
    #         print(obj)
    #     except:
    #         raise Http404("404")

    def download_and_convert(self):
        instance = self.get_object()
        video = instance.video_url
        print(f"&&&&&&&&&&&&&&&&&{video}")
        download(video)
        return redirect(f'/load-page-{instance.slug}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.download_and_convert()
        context["message"] = "Wait for download"
        return context


class LoadView(TemplateView):
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

# def index(request):
#     if request.method == 'POST':
#         form = YouTubeURLForm(request.POST)
#
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return HttpResponseRedirect('result-page')
#     else:
#         form = YouTubeURLForm()
#     return render(request, 'audio/index.html', {'form': form})
#
#
# def audio_page(request):
#     return render(request, 'audio/get_link.html')
