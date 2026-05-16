


import redis
import json


class CacheManager:
    def __init__(self):
        self.redis_client = None


    def init_app(self, app, *args, **kwargs):
        host = app.config.get("REDIS_HOST")
        port = app.config.get("REDIS_PORT")
        password = app.config.get("REDIS_PASSWORD")

        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            *args,
            **kwargs
        )


    def store_data(self, key, value, time_to_live=None):
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)

            if time_to_live is None:
                self.redis_client.set(key, value)
            else:
                self.redis_client.setex(key, time_to_live, value)
        except redis.RedisError as error:
            print(f"An error occurred while storing data in Redis: {error}")


    def check_key(self, key):
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                print(f"Key '{key}' exists in Redis.")
                ttl = self.redis_client.ttl(key)
                if ttl:
                    print(f"Key '{key}' has a TTL of {ttl}.")

                return True, ttl

            print(f"Key '{key}' does not exist in Redis.")
            return False, None
        except redis.RedisError as error:
            print(f"An error occurred while checking a key in Redis: {error}")
            return False, None


    def get_data(self, key):
        try:
            output = self.redis_client.get(key)
            if output is None:
                return None
            
            return json.loads(output)
        except redis.RedisError as error:
            print(f"An error occurred while retrieving data from Redis: {error}")


    def delete_data(self, key):
        try:
            output = self.redis_client.delete(key)
            if output > 0:
                print(f"Key '{key}' and its value have been deleted.")
            else:
                print(f"Key '{key}' not found.")

            return output == 1
        except redis.RedisError as error:
            print(f"An error occurred while deleting data from Redis: {error}")
            return False


    def delete_data_with_pattern(self, pattern):
        try:
            for key in self.redis_client.scan_iter(match=pattern):
                self.delete_data(key)
        except redis.RedisError as error:
            print(f"An error occurred while deleting data from Redis: {error}")	