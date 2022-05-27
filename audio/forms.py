from django import forms
from django.forms import ModelForm, URLField, URLInput, TextInput

from .models import Data


class YouTubeURLForm(ModelForm):
    video_url = forms.CharField(widget=forms.URLInput(), label='')

    class Meta:
        model = Data
        fields = ['video_url']
        # widgets = {'video_url': TextInput(attrs={'name': '', 'placeholder': 'Input your URL'})}
