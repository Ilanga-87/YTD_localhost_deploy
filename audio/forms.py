from django import forms
from django.forms import ModelForm

from .models import Conversion, SilentList


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

        if SilentList.objects.filter(confirmed_email=user_email):
            raise forms.ValidationError('Email in silent list', code='silent_list')

        if video_url[:16] != 'https://youtu.be' and video_url[:19] != 'https://www.youtube':
            raise forms.ValidationError('Please check your link', code='start_with')


class SilentListForm(ModelForm):
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your E-mail"}))

    class Meta:
        model = SilentList
        fields = ['user_email']

    def clean(self):
        cleaned_data = super(SilentListForm, self).clean()
        email = cleaned_data.get("user_email")

        if SilentList.objects.filter(confirmed_email=email):
            raise forms.ValidationError('This email is already in silent list', code='silent_list_exists')


class ConfirmationForm(ModelForm):

    class Meta:
        model = SilentList
        fields = ['user_email', 'input_code']

    def clean(self):
        cleaned_data = super(ConfirmationForm, self).clean()
        pk = self.instance.pk
        confirmation_code = cleaned_data.get("input_code")

        if SilentList.objects.get(pk=pk).confirmation_code != confirmation_code:
            raise forms.ValidationError('Wrong code', code='silent_list_confirmation')
