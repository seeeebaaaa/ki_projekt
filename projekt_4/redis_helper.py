from redis import Redis
from config.settings import REDIS_URL
import json


r = Redis.from_url(url=REDIS_URL, decode_responses=True)


def init_progress(uid):
    progress = {
        "state": "start",
        "state_text": "",
        "state_status": "",
        "task_state": "",
        "current_task_id": "",
    }
    save_progress(uid, progress)


def save_progress(uid, mapping):
    # redis cant use dicts with more than one depth, and lists etc. so just json it instead (see https://stackoverflow.com/questions/75157428/redis-exceptions-dataerror-invalid-input-of-type-dict-convert-to-a-bytes-s)
    current = get_progress(uid)
    combined = current | mapping # merge dictionarys, second one (new) replcaes old values
    dict_json = json.dumps(combined)
    r.hset(uid,key="data", value=dict_json)


def get_progress(uid):
    # redis cant use dicts with more than one depth, and lists etc. so just json it instead (see https://stackoverflow.com/questions/75157428/redis-exceptions-dataerror-invalid-input-of-type-dict-convert-to-a-bytes-s)
    dict_json = r.hget(uid,key="data")
    if dict_json:
        return json.loads(dict_json)
    else:
        return {}
