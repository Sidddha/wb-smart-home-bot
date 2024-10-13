FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /mnt/data/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /mnt/data/"${BOT_NAME:-tg_bot}"
RUN pip install -r /mnt/data/"${BOT_NAME:-tg_bot}"/requirements.txt
COPY . /mnt/data/"${BOT_NAME:-tg_bot}"
