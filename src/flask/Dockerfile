# pull official base image
FROM python:3.12.3

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

CMD ["flask","run", "--debug","--host=0.0.0.0","--port=5000"]