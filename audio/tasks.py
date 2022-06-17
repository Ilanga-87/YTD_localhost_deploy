from django.shortcuts import redirect
from youtube_dl import YoutubeDL
from youtube_dl.utils import YoutubeDLError

from YouTubeAudio.celery import app
from .models import Conversion
from .service import get_video_id


# from .service import mult

@app.task
def do_mult(a, b):
    return a * b


@app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def download(video, video_id):
    instance = Conversion.objects.get(slug=video_id)
    instance.video_url = video
    instance.video_id = video_id

    ytdl_opts = {
        "quiet": True,
        'cachedir': False,
        'outtmpl': 'uploads/audio/%(title)s.%(ext)s',
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
            audio = ydl.download([video])
            instance.audio_file.name = f"{instance.title}.mp3"
    except YoutubeDLError as err:
        print("Something get wrong")
        # TODO return error page
    # через ютдл из урла получить название видео + присвоить его title
    #
    # через дэйт тайм получиь таймстамп + присвоить его pub_time
    instance.save()
    return {"status": True}
