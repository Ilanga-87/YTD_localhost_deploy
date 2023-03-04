FROM python:3.10.8-alpine

# set work directory
WORKDIR /ytdmp3

# set environment variables
ENV PATH "$PATH:/mnt/d/PyCharm/ytd/YTD_deploy_1509"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## copy entrypoint
#COPY entrypoint .
#RUN sed -i 's/\r$//g' entrypoint
#RUN chmod +x entrypoint

# copy projec
COPY . .

## run entrypoint
#ENTRYPOINT ["sh", "entrypoint"]