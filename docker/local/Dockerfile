FROM python:3.11-alpine

WORKDIR /opt/StoreTracker

RUN apk update && apk upgrade

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./ ./

RUN pip install --upgrade pip && pip install -r requirements/local.txt
