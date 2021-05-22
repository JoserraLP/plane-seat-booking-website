from website import redis


def flush_db():
    # Delete all the data on the db
    redis.flush_db()
