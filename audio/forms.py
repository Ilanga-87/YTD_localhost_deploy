from django import forms


class YouTubeURLForm(forms.Form):
    your_url = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Input your URL'}))

