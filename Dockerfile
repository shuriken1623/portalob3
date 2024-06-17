FROM python:3.9

ENV PYTHONUNBUFFERTD 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt 

COPY . /code/

