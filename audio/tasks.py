from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from django.utils import timezone

from YouTubeAudio.celery import app
from .models import Conversion, SilentList
from .service import send_link, send_sad_letter


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
            instance.title = video_info.get("title", None)
            if video_info['duration'] >= 7200:
                message = 'ERROR: Video is longer then 2 hours'
                send_sad_letter(instance.user_email, message)
                instance.delete()

            else:
                ydl.download([video])
                instance.audio_file.name = f"{instance.title}.mp3"
                instance.save()
                link = f"https://my_site.com/load-audio-{instance.slug}"
                send_link(instance.user_email, link)
                return {"status": True}
    except YoutubeDLError as err:
        send_sad_letter(instance.user_email, err)
        instance.delete()


@app.task()
def clear_expired():
    now = timezone.now()
    Conversion.objects.filter(expiration_time__lt=now).delete()


@app.task()
def clear_empty():
    SilentList.objects.filter(confirmed_email__exact="").delete()
