FROM python:3.11-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/HealthNutrition-Backend

RUN apk update && \
    apk upgrade

COPY ./ ./

RUN pip install --upgrade pip &&  \
    pip install poetry

FROM base AS dev

RUN poetry config installer.max-workers 10 &&  \
    poetry install --without prod

FROM base AS prod

RUN poetry config installer.max-workers 10 &&  \
    poetry install --without dev
