FROM python:3.7.2-alpine3.8

COPY . /opt/app/
WORKDIR /opt/app

RUN apk update
RUN apk add python3-dev gcc libc-dev linux-headers

RUN pip install --upgrade pip --log /opt/app/pip_update.log
RUN python3 -m pip install -r requirements.txt --log /opt/app/pip_requirements.log

CMD python3 main.py
