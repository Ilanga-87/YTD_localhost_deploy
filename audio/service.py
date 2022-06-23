import datetime
import random
import string


def extract_single_from_playlist(video):
    splitted_url = video.split('&')
    return splitted_url[0]


def get_video_id(video):
    splitted_id = video.split("=")
    return splitted_id[-1]


def get_expiration_date():
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)
    return expiration_date.strftime("%d/%m/%Y %H:%M:%S")


def generate_slug_tail(length):
    char_set = string.ascii_letters + string.digits
    tail = ''.join(random.choice(char_set) for i in range(length))
    return tail
