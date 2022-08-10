from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, DetailView
from django.http import FileResponse

from .forms import YouTubeURLForm, BlackListForm, ConfirmationForm
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


class BlackListView(CreateView):
    model = SilentList
    form_class = BlackListForm
    template_name = 'audio/black_list.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        email = form.cleaned_data["user_email"]
        conf_code = generate_confirmation_code(4)
        instance.confirmation_code = conf_code
        send_confirmation_mail(email, conf_code)
        instance.save()
        return super(BlackListView, self).form_valid(form)

    def get_success_url(self):
        return reverse('confirm-blacklist', kwargs={'pk': self.object.pk})


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


class ConfirmedBlackListView(TemplateView):
    template_name = "audio/black_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmedBlackListView, self).get_context_data()
        context["message"] = "Now your email is in black list. We will never disturb you again."
        return context


class WaitContextView(TemplateView):
    template_name = "audio/black_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(WaitContextView, self).get_context_data()
        context["message"] = "Content is arriving... Please wait"
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"
