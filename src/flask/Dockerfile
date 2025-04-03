# pull official base image
FROM python:3.12.3
# set env variables for celery build comntext
# ARG CELERY_BROKER_URL
# ARG CELERY_RESULT_BACKEND
# ENV CELERY_BROKER_URL $CELERY_BROKER_URL
# ENV CELERY_RESULT_BACKEND $CELERY_RESULT_BACKEND

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /flask
WORKDIR /flask

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /flask

# initate celery
CMD ["celery", "-A", "app", "worker", "--loglevel", "INFO"]

# start flask
CMD ["flask","run", "--debug","--host=0.0.0.0","--port=5000"]