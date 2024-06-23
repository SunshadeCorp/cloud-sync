FROM python:3-buster

WORKDIR /usr/src/app

RUN pip install paho-mqtt~=1.5.1 PyYAML~=5.4.1 --no-cache-

COPY . .

CMD [ "python", "./cloud-sync.py" ]
