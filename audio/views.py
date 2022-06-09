from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from django.utils.text import slugify
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView

from pytils.translit import slugify as sg

from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from .forms import YouTubeURLForm
from .models import Conversion


# Create your views here.


def extract_single_from_playlist(video):
    splitted_url = video.split('&')
    return splitted_url[0]

def get_video_id(video):
    splitted_id = video.split("=")
    return splitted_id[-1]



class ConvertView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    template_name = "audio/index.html"
    success_url = "/success-page"

    def form_valid(self, form):
        instance = form.save(commit=False)
        print(f"***** THIS IS {instance}")
        video = extract_single_from_playlist(form.cleaned_data["video_url"])
        slug = get_video_id(video)
        print(slug)

        conversion = Conversion()
        conversion.slug = slug
        print(conversion.slug)
        conversion.video_url = video

        # пишем условие. если видео айди есть в базе данных, сразу редирект на страницу скачки. если нет, редирект на саксесс пэйдж
        if Conversion.objects.filter(video_id=conversion.slug).exists():
            return redirect(f"/load_audio_{conversion.slug}")

        SuccessView()

        # через ютдл из урла получить название видео + присвоить его title
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
                conversion.title = video_title
                audio = ydl.download([video])
                conversion.audio_file.name = f"upload/audio/{conversion.title}.mp3"

                print(f"***********{conversion.title}")
                print(f"++++++++ AND THIS IS {video_title}")
                print(f"SLUUUUUUUUG {conversion.slug}")
        except YoutubeDLError as err:
            print("Something get wrong")
            # TODO return error page



        # через дэйт тайм получиь таймстамп + присвоить его pub_time
        #TODO : if Book.objects.filter(user=self.user, title=title).exists():


        conversion.save()
        return redirect(f"/load_audio_{conversion.slug}")


class SuccessView(TemplateView):
    template_name = "audio/get_link.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Wait for download"
        return context


class LoadView(TemplateView):
    model = Conversion
    template_name = "audio/load_audio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Get it!"
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
