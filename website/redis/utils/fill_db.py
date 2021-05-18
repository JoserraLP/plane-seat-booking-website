from website.redis.utils.db.data_generator import DataGenerator

from website import redis

def fill_db():
    data_generator = DataGenerator()

    # Generating data
    data_generator.generate_data()

    # Retrieving data
    data = data_generator.get_data()

    redis.set(data)

    redis.bgsave()
