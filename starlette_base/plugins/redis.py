from dataclasses import dataclass

import redis as redis_sync
import redis.asyncio as redis_async
from starlette.config import Config

config = Config()


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int

    def __init__(self, host="localhost", port=6379, db=0):
        self.host = config("REDIS_HOST", cast=str, default=host)
        self.port = config("REDIS_PORT", cast=int, default=port)
        self.db = config("REDIS_DB", cast=int, default=db)


class RedisPlugin:
    def __init__(self, config_cls="RedisConfig", sync=False):
        self.config_cls = config_cls
        self.host = "localhost"
        self.port = 6379
        self.db = 0
        self._redis: redis_sync.Redis | redis_async.Redis = None
        self.sync = sync

    def register(self, app):
        config = app.config_loader.get(self.config_cls, None)
        if not config:
            raise RuntimeError(f"{self.config_cls} not found!")
        self.host = getattr(config, "host", self.host)
        self.port = getattr(config, "port", self.port)
        self.db = getattr(config, "db", self.db)
        if self._redis is None:
            if self.sync:
                pool = redis_sync.ConnectionPool(host=self.host, port=self.port, db=self.db)
                self._redis = redis_sync.Redis(connection_pool=pool)
            else:
                pool = redis_async.ConnectionPool(host=self.host, port=self.port, db=self.db)
                self._redis = redis_async.Redis(connection_pool=pool)

    def __getattr__(self, name):
        return getattr(self._redis, name)


rdb_async: redis_async.Redis = RedisPlugin(sync=False)

rdb_sync: redis_sync.Redis = RedisPlugin(sync=True)


def register(app):
    rdb_sync.register(app)
    rdb_async.register(app)
