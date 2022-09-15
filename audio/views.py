import logging

from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, DetailView
from django.http import FileResponse

from .forms import YouTubeURLForm, SilentListForm, ConfirmationForm
from .models import Conversion, SilentList
from .tasks import download
from .service import (
    extract_single_from_playlist,
    get_video_id,
    generate_slug_tail,
    get_expiration_date,
    send_link,
    send_confirmation_mail,
    generate_confirmation_code
)


# Create your views here.

class ConvertView(CreateView):
    model = Conversion
    form_class = YouTubeURLForm
    template_name = "audio/index.html"
    success_url = "/success-page"

    def form_valid(self, form):
        instance = form.save(commit=False)
        video = extract_single_from_playlist(form.cleaned_data["video_url"])
        video_id = get_video_id(video)
        slug_tail = generate_slug_tail(10)
        slug = slugify(f"{video_id}-{slug_tail}")
        instance.video_id = video_id
        instance.slug = slug

        possible_previous_conversion = Conversion.objects.filter(video_id=instance.video_id)
        if possible_previous_conversion and Conversion.objects.get(video_id=instance.video_id).audio_file.name != '':
            previous_conversion = Conversion.objects.get(video_id=instance.video_id)
            previous_conversion.expiration_time = get_expiration_date(1)
            previous_conversion.save()
            send_link(instance.user_email, previous_conversion.title, f"https://mp3-from-youtube.com/load-audio-{previous_conversion.slug}")
            return redirect(f"{self.success_url}-{previous_conversion.slug}")
        file_logger.info("TEST 00")
        instance.save()
        file_logger.info("TEST 01")
        download.delay(video, slug)
        file_logger.info("TEST 02")

        return redirect(f"{self.success_url}-{slug}")


class SuccessView(DetailView):
    model = Conversion
    template_name = "audio/success_page.html"


class LoadView(DetailView):
    model = Conversion
    template_name = "audio/load_audio.html"


def download_audio(request, title):
    audio_file = FileResponse(open(f'uploads/audio/{title}', 'rb'), as_attachment=True)
    return audio_file


class SilentListView(CreateView):
    model = SilentList
    form_class = SilentListForm
    template_name = 'audio/silent_list.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        email = form.cleaned_data["user_email"]
        conf_code = generate_confirmation_code(4)
        instance.confirmation_code = conf_code
        send_confirmation_mail(email, conf_code)
        instance.save()
        return super(SilentListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('confirm-silent-list', kwargs={'pk': self.object.pk})


class ConfirmationView(UpdateView):
    model = SilentList
    form_class = ConfirmationForm
    template_name_suffix = "_confirm"

    def form_valid(self, form):
        instance = form.save(commit=False)
        user_email = form.cleaned_data["user_email"]
        confirmation_code = form.cleaned_data["input_code"]
        if SilentList.objects.get(confirmation_code=confirmation_code):
            instance.confirmed_email = user_email
        instance.save()
        return super(ConfirmationView, self).form_valid(form)


class ConfirmedSilentListView(TemplateView):
    template_name = "audio/silent_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmedSilentListView, self).get_context_data()
        context["message"] = "Now your email is in silent list. We will never disturb you again."
        return context


class WaitContextView(TemplateView):
    template_name = "audio/silent_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(WaitContextView, self).get_context_data()
        context["message"] = "Content is arriving... Please wait"
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"


logger = logging.getLogger("thelogger")
file_logger = logging.getLogger("thelogger.file")


def index(request):
    logger.info(
        "This will be written to the console, should be seen in the gunicorn log"
    )
    file_logger.info(
        "This will be written to the file defined in the settings, given that the gunicorn has relevant rights"
    )
    return HttpResponse("The index")
