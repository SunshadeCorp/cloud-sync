FROM python:3-buster

WORKDIR /usr/src/app

RUN pip install paho-mqtt PyYAML

COPY . .

CMD [ "python", "./cloud-sync.py" ]
