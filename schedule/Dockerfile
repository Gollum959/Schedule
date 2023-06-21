FROM python:3.10.12-slim

RUN apt-get update &&\
    apt-get install -y libpq-dev gcc

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "schedule.wsgi:application", "--bind", "0:8000" ]
