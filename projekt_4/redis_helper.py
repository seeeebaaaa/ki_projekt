from redis import Redis
from config.settings import REDIS_URL


r = Redis.from_url(url=REDIS_URL)


def init_progress(uid):
    progress = {
        "state":"start",
        "state_text": "",
        "state_status": "",
        "current_task_id": None
    }
    save_progress(uid,progress)

def save_progress(uid,mapping):
    r.hset(uid,mapping=mapping)

def get_progress(uid):
    return r.hgetall(uid)
