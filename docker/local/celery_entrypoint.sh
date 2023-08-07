#!/bin/sh

poetry run celery -A core worker -l info -P eventlet
