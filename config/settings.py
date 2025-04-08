import os
from redis import Redis
from distutils.util import strtobool

# DO NOT EVER generate a key on the fly here, as each gunicorn
# worker will get a different secret, so every requests is outdated,
# as soon as it hits another worker
SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = bool(strtobool(os.getenv("FLASK_DEBUG", "false")))

SERVER_NAME = os.getenv(
    "SERVER_NAME", "localhost:{0}".format(os.getenv("PORT", "8000"))
)

# Redis.
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Celery.
CELERY_CONFIG = {
    "broker_url": REDIS_URL,
    "result_backend": REDIS_URL,
    "include": [],
    "task_ignore_result": True,
}

# flask sessions
SESSION_TYPE = "redis"
SESSION_REDIS = Redis.from_url(url=REDIS_URL)
SESSION_USE_SIGNER = True
