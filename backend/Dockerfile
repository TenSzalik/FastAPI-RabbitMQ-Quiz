FROM python:3.11.3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY requirements_dev.txt .
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

COPY . /app
