FROM python:3.11-alpine

WORKDIR /usr/src/StoreTracker

RUN apk update
RUN apk upgrade

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements ./requirements

RUN pip install --upgrade pip
RUN pip install -r requirements/local.txt

COPY ./ ./