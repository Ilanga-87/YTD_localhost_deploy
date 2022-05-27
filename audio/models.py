from django.db import models

# Create your models here.


class Data(models.Model):
    video_url = models.URLField('URL to Youtube')
    audio_url = models.CharField('URL to created audio', max_length=255)
    pub_time = models.TimeField('Publish time', blank=True, null=True)
