from django import forms


class YouTubeURLForm(forms.Form):
    your_url = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'Input your URL'}))

