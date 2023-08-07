# YouTube MP3 downloader

YouTube MP3 Downloader is a simple and straightforward tool for downloading MP3 files from YouTube. 
It comes with a Web UI built on Django and uses PostgreSQL as a database, Celery for deferred and scheduled tasks, and Redis as a broker. 
The downloading and conversion process is based on the "youtube-dlp" library.


![Python]({https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue})


## Installation

To install via Docker, follow these steps:

1. Download and install Docker from docker.com.

2. Clone this git repository by running the following command in your terminal:
```commandline
git clone --branch unlimited_time https://github.com/Ilanga-87/YTD_deploy/
```
3. Navigate to the project directory by using the "cd" command:

```commandline
cd YTD_deploy
```

4. Create a .env.dev file in the project directory and fill in the required variables:
```commandline
SQL_ENGINE=django.db.backends.postgresql
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
SECRET_KEY=change_me *
SQL_DATABASE=db_name *
SQL_USER=db_user *
SQL_PASSWORD=db_password *
EMAIL_U=email *
EMAIL_P=email_password *
DJANGO_ALLOWED_HOSTS=127.0.0.1
CSRF_TRUSTED=http://127.0.0.1
```

Replace the values marked with "*" with appropriate values, 
and if launching the service on a specialized domain, provide the domain for "DJANGO_ALLOWED_HOSTS" and "CSRF_TRUSTED."

**Attention:** Please note that the email_password is not your standard password used for logging in and checking emails.

To enable the application's email functionality, you need to provide the necessary authentication credentials. 
Depending on your mail provider, this can be done using a token, access key, or another authentication variant. 
This step allows the application to securely interact with your email account for sending and receiving messages.

Please follow the instructions provided by your email service provider to generate the required authentication credentials. 
Once obtained, you will integrate these credentials into the application's settings to enable seamless email communication.

5. Create a ".env.db" file with the same variables used in the previous step:
```commandline
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
POSTGRES_DB=db_name
```

6. To build production images and run containers, use the following command:
```
docker compose up --build -d
```

7. To create an admin user, execute the following command:
```
docker compose exec ytd python manage.py createsuperuser
```

## Usage

Once the installation is complete, open your preferred web browser and visit http://127.0.0.1:8000 to access the YouTube MP3 downloader service.

Please note that this service allows to download MP3 files from YouTube videos for personal use only, 
and you should comply with YouTube's terms of service and any applicable copyright laws.



## Features

- Download MP3 files from YouTube videos.
- Option to add user email to the silent list to prevent potential email spam from the service.
- Automatic disk space cleanup by deleting files and database instances older than 24 hours. The cleansing task runs every midnight.

If you encounter any issues or have questions, feel free to reach out for support.