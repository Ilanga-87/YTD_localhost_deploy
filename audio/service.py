def extract_single_from_playlist(video):
    splitted_url = video.split('&')
    return splitted_url[0]


def get_video_id(video):
    splitted_id = video.split("=")
    return splitted_id[-1]

