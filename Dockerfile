FROM python:3.10.11-bullseye

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt install nano mc -qy

WORKDIR /opuser

COPY inflect.py .
COPY morph.py .
COPY requirements.txt .

RUN pip install -r requirements.txt