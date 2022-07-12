# YouTubeAudioDownloader

This is a website that allows you to download mp3 audio files from YouTube video

To install it you should have Python3 on your device. Also, you need install REDIS and PostgreSQL. 
Pay attention that there are default host and port for REDIS in settings.py (127.0.0.1:6379).

## Create database and user
```
CREATE DATABASE db_name OWNER user_name;
```
Open settings.py in YouTubeAudio folder and find follow

```Python3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

Here you should fill name of your database, user and password.

## Create and activate virtual environment
After cloning the repo you’re better to delete venv folder. Then create new venv according your Python3 version.
In command line move to YouTubeAudio folder and enter the next command
```
python3 -m venv /path/to/new/virtual/environment
```
Then activate it.

Windows CMD:
```
<venv>\Scripts\activate.bat
```
Linux bash:
```
source <venv>/bin/activate
```
## Get necessary modules
```
pip install -r requirements.txt
```

## Start on localhost
```
python3 manage.py runserver
```
Now you can open site by http://127.0.0.1:8000/ 

## Start tasks
In separate terminals in project folder with activated virtual environment input next commands
```
celery -A YouTubeAudio worker -P gevent -l info
```
```
celery -A YouTubeAudio beat -l info
```
Also you can start flower for tracking
```
celery --broker=redis://127.0.0.1:6379/0 flower  --port=5555
```

## Change email
In settings.py input your email and password 
```Pytnon3
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
```
If you don’t use Gmail you also have to change host and may be some other parameters. 

