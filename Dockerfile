FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /mnt/data/${BOT_NAME}

COPY requirements.txt /mnt/data/${BOT_NAME}
RUN pip install -r /mnt/data/${BOT_NAME}/requirements.txt
COPY . /mnt/data/${BOT_NAME}
