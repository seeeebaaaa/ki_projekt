# pull official base image
FROM python:3.12.3 AS parser


RUN mkdir -p /sp_docu
WORKDIR /sp_docu

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /sp_docu

CMD ["fastapi","dev","--host=0.0.0.0","--port=7000", "app.py"]