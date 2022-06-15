from YouTubeAudio.celery import app


# from .service import mult

@app.task
def do_mult(a, b):
    return a * b
