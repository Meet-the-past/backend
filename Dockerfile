# pull official base image
FROM --platform=linux/x86_64 python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG DJANGO_ALLOWED_HOSTS
ARG DJANGO_SECRET_KEY
ARG DJANGO_CORS_ORIGIN_WHITELIST

ENV DJANGO_ALLOWED_HOSTS $DJANGO_ALLOWED_HOSTS
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
ENV DJANGO_CORS_ORIGIN_WHITELIST $DJANGO_CORS_ORIGIN_WHITELIST

WORKDIR /backend
COPY requirements.txt /backend/

# RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y


# RUN apt add postgresql-dev libressl-dev libffi-dev gcc musl-dev gcc python3-dev musl-dev zlib-dev jpeg-dev #--(5.2)


RUN pip install --upgrade pip

#AI
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
RUN pip install cmake
RUN pip3 install dlib



COPY . /backend/