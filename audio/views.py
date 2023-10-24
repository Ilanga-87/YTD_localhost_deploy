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


class AboutView(TemplateView):
    template_name = "about.html"
    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data()
        linkedin_url = "https://www.linkedin.com/in/%D0%BB%D0%B8%D0%BA%D0%B0-%D1%80%D0%BE%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2%D0%B0-0a7134298/"
        repo_url = "https://github.com/Ilanga-87/YTD_localhost_deploy"
        github_url = "https://github.com/Ilanga-87"
        email_address = "mp3.from.ytb@gmail.com"
        context["linkedin_url"] = linkedin_url
        context["repo_url"] = repo_url
        context["github_url"] = github_url
        context["email"] = email_address
        return context
