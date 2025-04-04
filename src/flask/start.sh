# initate celery
celery -A app.celery_app worker --loglevel INFO &
# start flask
flask run --debug --host=0.0.0.0 --port=5000