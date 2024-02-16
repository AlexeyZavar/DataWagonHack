FROM matthewfeickert/docker-python3-ubuntu:3.10.5

WORKDIR /app

USER root

RUN apt-get update && apt-get install --no-install-recommends --fix-missing -y \
    curl \
    build-essential \
    rustc \
    cargo \
    locales \
    libpq-dev
RUN locale-gen ru_RU.UTF-8
RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen
RUN sed -i 's/^# *\(ru_RU.UTF-8\)/\1/' /etc/locale.gen
RUN locale-gen

ENV LANG=ru_RU.UTF-8

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . /app

STOPSIGNAL SIGKILL
ENTRYPOINT python prod.py
