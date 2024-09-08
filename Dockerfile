FROM python:3.11.3-slim

WORKDIR /app

COPY ./requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .