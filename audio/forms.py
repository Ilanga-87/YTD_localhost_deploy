from django import forms
from django.forms import ModelForm, URLField, URLInput, TextInput

from .models import Conversion


def start_with(value):
    if value[:19] != 'https://www.youtube':
        raise forms.ValidationError('Please check your link')


class YouTubeURLForm(ModelForm):
    video_url = forms.CharField(widget=forms.URLInput(attrs={"placeholder": "YouTube URL"}), label='')
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your E-mail"}))

    class Meta:
        model = Conversion
        fields = ['video_url', 'user_email']
        # widgets = {'video_url': TextInput(attrs={'name': '', 'placeholder': 'Input your URL'})}
