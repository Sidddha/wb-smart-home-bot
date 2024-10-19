FROM python:3.9-buster

 
WORKDIR /mnt/data/wb-smart-home-bot

COPY requirements.txt /mnt/data/wb-smart-home-bot
RUN pip install -r /mnt/data/wb-smart-home-bot/requirements.txt
COPY . /mnt/data/wb-smart-home-bot

ENTRYPOINT ["python3", "-m", "app"]
