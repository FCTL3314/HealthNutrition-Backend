FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/StoreTracker

RUN apk update && \
    apk upgrade

COPY ./ ./

RUN pip install --upgrade pip &&  \
    pip install poetry

RUN poetry config installer.max-workers 10 &&  \
    poetry install
