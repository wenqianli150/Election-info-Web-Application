FROM python:3.9-slim-buster

COPY . .
RUN apt-get update 
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

