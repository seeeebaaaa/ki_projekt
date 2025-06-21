# pull official base image
FROM python:3.12.3-slim AS prompter


RUN mkdir -p /parser
WORKDIR /parser

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /parser

CMD ["fastapi","dev","--host=0.0.0.0","--port=6000", "app.py"]