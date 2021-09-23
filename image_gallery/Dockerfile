FROM python:3.7.11-slim

ADD . /app

WORKDIR /app

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

EXPOSE 5000

CMD waitress-serve --host=0.0.0.0 --port=5000 main:app
