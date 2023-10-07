import os
from dotenv import load_dotenv

from yt_dlp import YoutubeDL
from yt_dlp.utils import YoutubeDLError

from django.utils import timezone

from YouTubeAudio.celery import app
from .models import Conversion, SilentList
from .service import send_link, send_sad_letter, extract_single_from_playlist, clear_title

load_dotenv()


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def download(video, video_id):
    """The function that download and convert video to mp3 file by ytdl module"""
    instance = Conversion.objects.get(slug=video_id)
    instance.video_url = video

    new_title = ''

    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
    }
    try:
        with YoutubeDL(ytdl_opts) as ydl:
            track_url = extract_single_from_playlist(video)
            video_info = ydl.extract_info(track_url, download=False)
            title = video_info['title']
            new_title += clear_title(title)

    except YoutubeDLError:
        send_sad_letter(instance.user_email, instance.title)
        instance.delete()

    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': f'uploads/audio/{new_title}.%(ext)s',
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
            instance.title = video_info.get("title", None)

            ydl.download([video])
            instance.audio_file.name = f"{new_title}.mp3"
            instance.save()
            sitename = os.environ.get('DOMAIN', '127.0.0.1:8000')
            link = f"{sitename}/load-audio-{instance.slug}"
            send_link(instance.user_email, instance.title, link)
            return {"status": True}
    except YoutubeDLError:
        send_sad_letter(instance.user_email, instance.title)
        instance.delete()


@app.task()
def clear_expired():
    """Delete expired files and db instances"""
    now = timezone.now()
    Conversion.objects.filter(expiration_time__lt=now).delete()


@app.task()
def clear_empty():
    """Delete unconfirmed emails"""
    SilentList.objects.filter(confirmed_email__exact="").delete()
