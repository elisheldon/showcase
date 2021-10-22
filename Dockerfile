# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /showcase
COPY requirements.txt /showcase/
RUN pip install -r requirements.txt
COPY . /showcase/