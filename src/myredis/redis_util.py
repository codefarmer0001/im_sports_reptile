import redis
from config import CONFIG


class redis_util:

    def __init__(self) -> None:
        self.r = redis.Redis(host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=CONFIG.REDIS_DB, password=CONFIG.REDIS_PASSWORD)
        pass


    def set_string(self, key, value):
        self.r.set(f'time_{key}', value)

    def get_string(self, key):
        value = self.r.get(f'time_{key}')
        return value.decode('utf-8')