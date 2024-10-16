FROM python:3.9-buster
ARG BOT_NAME
ENV BOT_NAME=${BOT_NAME}

WORKDIR /mnt/sdcard/${BOT_NAME}

COPY requirements.txt /mnt/sdcard/${BOT_NAME}
RUN pip install -r /mnt/sdcard/${BOT_NAME}/requirements.txt
COPY . /mnt/sdcard/${BOT_NAME}
