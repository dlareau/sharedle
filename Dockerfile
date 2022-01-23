FROM node:17
RUN apt-get update || : && apt-get install python -y
RUN apt-get install python3-pip -y

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENABLE_DEBUG False
ENV DJANGO_SETTINGS_MODULE sharedle.settings.env_settings

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py tailwind install
RUN python3 manage.py tailwind build

EXPOSE 8000
CMD ["gunicorn", "--workers=5", "--bind=0.0.0.0:8000", "puzzlehunt_server.wsgi:application"]