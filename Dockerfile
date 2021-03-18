FROM python:3.8.7-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0

# install psycopg2
#RUN apk update

#RUN apk update \
#    && apk add --virtual build-deps gcc python3-dev musl-dev \
#    && apk add postgresql-dev \
#    && pip install psycopg2 \
#    && apk del build-deps

# start to install backend-end stuff
WORKDIR /app

# Install Python requirements.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code.
COPY . .

# add and run as non-root user
#RUN adduser -D myuser
#USER myuser

#
RUN python manage.py collectstatic --noinput

# run gunicorn
#CMD gunicorn lib_project.wsgi:application --bind 0.0.0.0:$PORT
CMD gunicorn lib_project.wsgi:application
