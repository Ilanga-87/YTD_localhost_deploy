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


def generate_confirmation_code(length):
    char_set = string.ascii_uppercase + string.digits
    conf_code = ''.join(random.choice(char_set) for i in range(length))
    return conf_code


def send_link(user_mail, link):
    expiration_time = get_expiration_date()
    send_mail(
        "Your audio is ready to download",
        f"Hi, here is a link where you can get your mp3 file:\n\n\t{link} \n\n It will be actual till {expiration_time.strftime('%d/%b/%Y %H:%M:%S')}. \n\nBest regards, mysite.com.\n\n You've received this email because it was entered on mysite.com. Don't want to receive our emails? Please, add your email into silent list here: mysite.com/do-not-disturb.",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


def send_sad_letter(user_mail, error):
    send_mail(
        "Sorry, but something got wrong",
        f"Hi, we are unfortunate, but your mp3 conversion went wrong. Here is the description of problem:\n\n\t {error} \n\nBest regards, mysite.com.\n\n You've received this email because it was entered on mysite.com. Don't want to receive our emails? Please, add your email to the silent list here: mysite.com/do-not-disturb.",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )


def send_confirmation_mail(user_mail, conf_code):
    send_mail(
        "Confirm your email",
        f"Hi, your confirmation code is \n\n\t {conf_code} \n\nIf you don't have any idea about this letter just delete it. \n\nBest regards, mysite.com",
        settings.EMAIL_HOST_USER,
        [user_mail]
    )
