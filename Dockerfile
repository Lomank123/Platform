FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV APP_DIR=/app
ENV APP_USER=platform_user

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc git libc-dev python3-dev pkg-config libpq-dev postgresql \
    && apt-get clean

WORKDIR $APP_DIR

COPY . .

RUN pip install -r requirements.txt \
    && useradd -ms /bin/bash $APP_USER \
    && chown -R $APP_USER:$APP_USER $APP_DIR

USER $APP_USER