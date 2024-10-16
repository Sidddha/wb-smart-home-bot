FROM python:3.9-buster
ARG BOT_NAME
ENV BOT_NAME=$BOT_NAME
 
WORKDIR /mnt/data/$BOT_NAME

COPY requirements.txt /mnt/data/$BOT_NAME/requirements.txt
RUN pip install -r /mnt/data/$BOT_NAME/requirements.txt
COPY . /mnt/data/$BOT_NAME
