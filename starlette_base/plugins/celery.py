import logging
from copy import deepcopy

from celery import Celery

DEFAULT_CELERY_CONFIG = {
    "broker_url": "redis://localhost:6379/10",
    "broker_connection_retry_on_startup": True,
    "timezone": "Asia/Shanghai",
    "broker_transport_options": {
        "fanout_prefix": True,
        "fanout_patterns": True,
        "visibility_timeout": 3600,
    },
    "imports": [],
    "soft_time_limit": 3600,
    "beat_schedule": {},
}


class CeleryPlugin:
    def __init__(self, config_name="CELERY_CONFIG"):
        self._celery = None
        self._config_name = config_name
        self._initialized = False

    def register(self, app) -> Celery:
        if self._initialized:
            return self._celery
        if self._celery is not None:
            return self._celery
        config = app.config_loader.get(self._config_name)
        if not config:
            raise RuntimeError("celery config not found!")
        if missing := (set(DEFAULT_CELERY_CONFIG.keys()) - set(config.keys())):
            raise RuntimeError(f"celery config invalid! missing keys: {missing}")
        config = deepcopy(config)
        self._celery = Celery(__name__, broker=config["broker_url"])
        self._celery.conf.update(config)
        self._initialized = True
        logging.warning("--- Celery initialized.")
        return self._celery

    @property
    def celery(self) -> Celery:
        return self._celery
