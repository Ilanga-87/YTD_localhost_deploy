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
    send_confirmation_mail,
    generate_confirmation_code
)


# Create your views here.

class ConvertView(CreateView):
    """The view for main page"""
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

        # possible_previous_conversion = Conversion.objects.filter(video_id=instance.video_id)
        # if possible_previous_conversion and Conversion.objects.get(video_id=instance.video_id).audio_file.name != '':
        #     previous_conversion = Conversion.objects.get(video_id=instance.video_id)
        #     previous_conversion.expiration_time = get_expiration_date(1)
        #     previous_conversion.save()
        #     send_link(instance.user_email, previous_conversion.title, f"https://mp3-from-youtube.com/load-audio-{previous_conversion.slug}")
        #     return redirect(f"{self.success_url}-{previous_conversion.slug}")
        instance.save()
        download.delay(video, slug)  # deferred processing

        return redirect(f"{self.success_url}-{slug}")


class SuccessView(DetailView):
    """Return page for redirection in case of correct form filling"""
    model = Conversion
    template_name = "audio/success_page.html"


class LoadView(DetailView):
    """Return page with link to audio"""
    model = Conversion
    template_name = "audio/load_audio.html"


def download_audio(request, title):
    """The function that give the audio to user"""
    audio_file = FileResponse(open(f'uploads/audio/{title}', 'rb'), as_attachment=True)
    return audio_file


class SilentListView(CreateView):
    """Return the form to adding email in silent list"""
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
    """Here user must confirm his email to add it in silent list"""
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
    """Return page in case of success adding to silent list"""
    template_name = "audio/silent_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmedSilentListView, self).get_context_data()
        context["message"] = "Now your email is in silent list. We will never disturb you again."
        return context


class WaitContextView(TemplateView):
    """Just dummy template view for pages without content"""
    template_name = "audio/silent_list_thank_you.html"

    def get_context_data(self, **kwargs):
        context = super(WaitContextView, self).get_context_data()
        context["message"] = "Content is arriving... Please wait"
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"
