from datetime import timedelta

import redis
import website.static.constants as constants


class RedisDB:

    def __init__(self, host='localhost', port=6379, db=0, password=constants.REDIS_PASSWORD):

        # Default db is 0
        self.r = redis.Redis(host=host, port=port, db=db, password=password)

    def set(self, data):
        # We make it with pipelines because it is more efficient
        with self.r.pipeline() as pipe:
            for item in data:
                for key, value in item.items():
                    pipe.hmset(key, value)
            pipe.execute()

    def update(self, name, key, value):
        self.r.hset(name=name, key=key, value=value)

    def bgsave(self):
        self.r.bgsave()

    def get(self, key, attr=None):
        if attr:
            return {k.decode("utf-8"): v.decode("utf-8") for k, v in self.r.hget(key, attr).items()}
        else:
            return {k.decode("utf-8"): v.decode("utf-8") for k, v in self.r.hgetall(key).items()}

    def get_key(self, key):
        return self.r.get(key).decode("utf-8")

    def get_all_keys(self):
        return [key.decode("utf-8") for key in self.r.keys()]

    def flush_db(self):
        self.r.flushdb()

    def set_key_expiry(self, key, minutes):
        self.r.setex(name=key, time=timedelta(minutes=minutes), value="...")
