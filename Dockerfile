FROM python:3.10.8-alpine

# set work directory
ENV HOME=/home/deploy
ENV APP_HOME=/home/deploy/ytd
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# create directory for the deploy user
RUN mkdir -p /home/deploy

# create the deploy user
RUN addgroup -S deploy && adduser -S deploy -G deploy

# create the appropriate directories
RUN mkdir $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/uploads/audio
RUN mkdir -p $APP_HOME/celery/var/run/celerybeat-schedule
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade yt-dlp
RUN apk update && apk upgrade && apk add ffmpeg

# copy entrypoint
COPY entrypoint .
RUN sed -i 's/\r$//g' entrypoint
RUN chmod +x entrypoint

# copy project
COPY . $APP_HOME

# chown all the files to the deploy user
RUN chown -R deploy:deploy $APP_HOME

# change to the deploy user
USER deploy

# run entrypoint
ENTRYPOINT ["sh", "entrypoint"]
