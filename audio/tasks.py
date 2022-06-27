from pytils.translit import slugify as sg
from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError
import datetime

from YouTubeAudio.celery import app
from .models import Conversion
from django.conf import settings
from django.core.mail import send_mail
from .service import get_expiration_date


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def download(video, video_id):
    instance = Conversion.objects.get(slug=video_id)
    instance.video_url = video

    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': f'uploads/audio/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            video_info = ydl.extract_info(video, download=False)
            video_title = video_info.get("title", None)
            instance.title = video_title
            # TODO if video_info['duration'] >= 18000
            audio = ydl.download([video])
            instance.audio_file.name = f"{instance.title}.mp3"
    except YoutubeDLError as err:
        print("Something get wrong")
        # TODO return error page
    # через дэйт тайм получиь таймстамп + присвоить его pub_time
    instance.save()
    return {"status": True}


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def send_link(user_mail, link):
    expiration_time = get_expiration_date()
    send_mail(
        "Your audio is ready to download",
        f"Hi, here is a {link} where you can get your mp3 file. It will be actual till {expiration_time.strftime('%d/%m/%Y %H:%M:%S')}. If you don't sense what is it, follow that link https://my_site.com/ and we will not disturb you more ",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
    return expiration_time


@app.task()
def clear_expired():
    now = datetime.datetime.now()
    Conversion.objects.filter(expiration_time__lt=now).delete()