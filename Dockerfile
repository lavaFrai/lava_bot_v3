FROM python:3.9.16-alpine3.17

COPY . /opt/app/
WORKDIR /opt/app

RUN apk update
RUN apk add python3-dev gcc libc-dev linux-headers

RUN pip install --upgrade pip --log /opt/app/pip_update.log
RUN python3 -m pip install -r requirements.txt --log /opt/app/pip_requirements.log

CMD python3 main.py
