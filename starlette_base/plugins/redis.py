import logging
from copy import deepcopy

import redis as redis_sync
import redis.asyncio as redis_async

DEFAULT_REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}


class RedisPlugin:
    def __init__(self, config_name="REDIS_CONFIG", sync=False):
        self._config_name = config_name
        self._redis: redis_sync.Redis | redis_async.Redis = None
        self.sync = sync
        self._initialized = False

    def register(self, app):
        if self._initialized:
            return self._redis
        config = app.config_loader.get(self._config_name, None)
        if not config:
            raise RuntimeError("redis config not found!")
        if missing := (set(DEFAULT_REDIS_CONFIG.keys()) - set(config.keys())):
            raise RuntimeError(f"redis config invalid! missing keys: {missing}")

        config = deepcopy(config)

        self.host = config["host"]
        self.port = config["port"]
        self.db = config["db"]

        if self._redis is None:
            if self.sync:
                pool = redis_sync.ConnectionPool(host=self.host, port=self.port, db=self.db)
                self._redis = redis_sync.Redis(connection_pool=pool)
            else:
                pool = redis_async.ConnectionPool(host=self.host, port=self.port, db=self.db)
                self._redis = redis_async.Redis(connection_pool=pool)
        self._initialized = True
        logging.warning("--- Redis client initialized.")
        return self._redis

    @property
    def redis(self):
        return self._redis
