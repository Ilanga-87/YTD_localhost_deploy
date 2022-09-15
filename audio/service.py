from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import random
import string
import datetime


def extract_single_from_playlist(video: str) -> str:
    """Get URL to single track from playlist, channel or another instance."""
    splitted_url = video.split('&')
    return splitted_url[0]


def get_video_id(video: str) -> str:
    """Get ID of downloading video for desktop URLS."""
    splitted_id = video.split("=")
    return splitted_id[-1]


def get_expiration_date(delta: int) -> datetime.datetime:
    """Calculate date and time of expiration of audio file."""
    expiration_date = timezone.now() + datetime.timedelta(days=delta)
    return expiration_date


def generate_slug_tail(length: int) -> str:
    """Generate unique addition to slug."""
    char_set = string.ascii_lowercase + string.digits
    tail = ''.join(random.choice(char_set) for i in range(length))
    return tail


def generate_confirmation_code(length: int) -> str:
    """Generate unique confirmation code for blacklist."""
    char_set = string.ascii_uppercase + string.digits
    conf_code = ''.join(random.choice(char_set) for i in range(length))
    return conf_code


def send_link(user_mail: str, link: str, title: str) -> None:
    """Send email with link to download audio."""
    expiration_time = get_expiration_date(1)
    send_mail(
        "Your audio is ready to download",
        f"Hi, here is a link where you can get your mp3 file {title}:\n\n\t{link} \n\nIt will be actual till {expiration_time.strftime('%d/%b/%Y %H:%M:%S')}. \n\nBest regards, MP3 from YouTube.\n\nYou've received this email because it was entered on https://mp3-from-youtube.com/. Don't want to receive our emails? Please, add your email into silent list here: https://mp3-from-youtube.com/do-not-disturb",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


def send_sad_letter(user_mail: str, title: str, error: str = '') -> None:
    """Send email in case of error."""
    send_mail(
        "Sorry, but something got wrong",
        f"Hi, we are unfortunate, but your mp3 conversion {title} went wrong{error}. Please check your link and try again. \n\nBest regards, MP3 from YouTube.\n\nYou've received this email because it was entered on https://mp3-from-youtube.com/. Don't want to receive our emails? Please, add your email to the silent list here: https://mp3-from-youtube.com/do-not-disturb.",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


def send_confirmation_mail(user_mail: str, conf_code: str) -> None:
    """Send email with unique code."""
    send_mail(
        "Confirm your email",
        f"Hi, your confirmation code for MP3 from YouTube is \n\n\t {conf_code} \n\nIf you don't have any idea about this letter just delete it. \n\nBest regards, MP3 from YouTube.",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
