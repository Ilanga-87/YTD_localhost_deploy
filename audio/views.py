from django.shortcuts import redirect
from django.utils.text import slugify
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.conf import settings
from django.http import FileResponse

import redis

from .forms import YouTubeURLForm, BlackListForm, ConfirmationForm
from .models import Conversion
from .tasks import download
from .service import extract_single_from_playlist, get_video_id, generate_slug_tail, \
    get_expiration_date, send_link, send_confirmation_mail, generate_confirmation_code


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
            previous_conversion.expiration_time = get_expiration_date()
            previous_conversion.save()
            send_link(instance.user_email, f"https://my_site.com/load-audio-{previous_conversion.slug}")
            return redirect(f"{self.success_url}-{previous_conversion.slug}")

        instance.save()
        download.delay(video, slug)

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


response_for_black_list = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2, charset='utf-8', decode_responses=True)
email_black_list = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, charset='utf-8', decode_responses=True)


class BlackListView(FormView):
    template_name = 'audio/black_list.html'
    success_url = '/confirm-blacklist'
    form_class = BlackListForm

    def form_valid(self, form):
        email = form.cleaned_data["user_email"]
        conf_code = generate_confirmation_code(4)
        response_for_black_list.set(conf_code, email)
        send_confirmation_mail(email, conf_code)
        return super(BlackListView, self).form_valid(form)


class ConfirmationView(FormView):
    template_name = "audio/black_list_confirm.html"
    success_url = '/confirmed'
    form_class = ConfirmationForm

    def form_valid(self, form):
        conf_code = form.cleaned_data["conf_code"]
        email_black_list.set(response_for_black_list.getdel(conf_code), conf_code)
        return super(ConfirmationView, self).form_valid(form)


class ConfirmedBL(TemplateView):
    template_name = "audio/black_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmedBL, self).get_context_data()
        context["message"] = "Now your email is in black list. We will never disturb you again."
        return context


class WaitContext(TemplateView):
    template_name = "audio/black_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(WaitContext, self).get_context_data()
        context["message"] = "Content is arriving... Please wait"
        return context
