FROM python:3.13.2-slim-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get install python3-dev build-essential pkg-config vim -y

# RUN apt-get update \
#     && apt-get install python3-dev build-essential pkg-config gettext -y

RUN pip install --upgrade pip 

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 8000