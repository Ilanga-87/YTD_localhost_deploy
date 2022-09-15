from django.db import models
from django.urls import reverse

from .service import get_expiration_date


# Create your models here.


class Conversion(models.Model):
    user_email = models.EmailField(max_length=254, default="")
    video_id = models.CharField("ID video", default="", max_length=100)
    video_url = models.CharField('URL to Youtube', max_length=255)
    title = models.CharField('Video title', max_length=100, blank=True)
    audio_url = models.CharField('URL to created audio', max_length=255, blank=True)
    pub_time = models.DateTimeField('Publish time', auto_now_add=True)
    slug = models.SlugField(default=" ", max_length=255, blank=True, null=False)
    audio_file = models.FileField(upload_to="audio", blank=True)
    expiration_time = models.DateTimeField('Burn time', default=get_expiration_date)

    def __str__(self):
        return self.title


class SilentList(models.Model):
    user_email = models.EmailField(max_length=256)
    confirmation_code = models.CharField(max_length=4)
    input_code = models.CharField(max_length=4, default="")
    confirmed_email = models.EmailField(max_length=256, default="")

    def get_absolute_url(self):
        return reverse('confirmed-silent-list', kwargs={'pk': self.pk})
