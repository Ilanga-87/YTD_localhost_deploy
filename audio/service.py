from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

import random
import string
import datetime


def extract_single_from_playlist(video):
    splitted_url = video.split('&')
    return splitted_url[0]


def get_video_id(video):
    splitted_id = video.split("=")
    return splitted_id[-1]


def get_expiration_date():
    expiration_date = timezone.now() + datetime.timedelta(days=1)
    return expiration_date


def generate_slug_tail(length):
    char_set = string.ascii_lowercase + string.digits
    tail = ''.join(random.choice(char_set) for i in range(length))
    return tail


def send_link(user_mail, link):
    expiration_time = get_expiration_date()
    send_mail(
        "Your audio is ready to download",
        f"Hi, here is a {link} where you can get your mp3 file. It will be actual till {expiration_time.strftime('%d/%b/%Y %H:%M:%S')}. If you don't sense what is it, follow that link https://my_site.com/ and we will not disturb you more ",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


def send_sad_letter(user_mail, error):
    send_mail(
        "Sorry, but something got wrong",
        f"Hi, we are very sad, but your mp3 conversion gone wrong. Here is the description of problem:\n\n \t {error}",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
