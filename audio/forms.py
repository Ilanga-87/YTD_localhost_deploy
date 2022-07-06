from django import forms
from django.forms import ModelForm, Form
from django.conf import settings

import redis

from .models import Conversion

response_for_black_list = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2, charset='utf-8', decode_responses=True)
email_black_list = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, charset='utf-8', decode_responses=True)


class YouTubeURLForm(ModelForm):
    video_url = forms.CharField(widget=forms.URLInput(attrs={"placeholder": "YouTube URL"}), label='')
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your E-mail"}))

    class Meta:
        model = Conversion
        fields = ['video_url', 'user_email']

    def clean(self):
        cleaned_data = super(YouTubeURLForm, self).clean()
        video_url = cleaned_data.get("video_url")
        user_email = cleaned_data.get("user_email")

        if email_black_list.exists(user_email):
            raise forms.ValidationError('Email in black list', code='black_list')

        if video_url[:16] != 'https://youtu.be' and video_url[:19] != 'https://www.youtube':
            raise forms.ValidationError('Please check your link', code='start_with')


class BlackListForm(Form):
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your E-mail"}))

    def clean(self):
        cleaned_data = super(BlackListForm, self).clean()
        email = cleaned_data.get("user_email")

        if email_black_list.exists(email):
            raise forms.ValidationError('This email is already in black list', code='black_list_exists')


class ConfirmationForm(Form):
    conf_code = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super(ConfirmationForm, self).clean()
        conf_code = cleaned_data.get("conf_code")

        if not response_for_black_list.exists(conf_code):
            raise forms.ValidationError('Wrong code', code='black_list_confirmation')
