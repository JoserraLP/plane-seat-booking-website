from website.redis.utils.db.data_generator import DataGenerator

from website import redis, redis_lock

def flush_db():

    # Delete all the data on the db
    redis.flush_db()

    # Delete all the data on the db
    redis_lock.flush_db()
