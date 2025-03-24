from dataclasses import asdict, dataclass

from celery import Celery
from starlette.config import Config

config = Config()


@dataclass
class CeleryConfig:
    broker_url: str
    broker_connection_retry_on_startup: bool
    timezone: str
    broker_transport_options: dict
    imports: list
    soft_time_limit: int
    beat_schedule: dict = None

    def __init__(
        self,
        broker_url="redis://localhost:6379/10",
        broker_connection_retry_on_startup=True,
        timezone="Asia/Shanghai",
        broker_transport_options=None,
        imports=None,
        soft_time_limit=3600,
        beat_schedule=None,
    ):
        self.broker_url = config("CELERY_BROKER_URL", cast=str, default=broker_url)
        self.broker_connection_retry_on_startup = broker_connection_retry_on_startup
        self.timezone = config("CELERY_TIMEZONE", cast=str, default=timezone)
        self.broker_transport_options = broker_transport_options or {
            "fanout_prefix": True,
            "fanout_patterns": True,
            "visibility_timeout": 3600,
        }
        self.imports = imports or []
        self.soft_time_limit = soft_time_limit
        self.baet_schedule = beat_schedule or {}


class CeleryPlugin:
    def __init__(self, config_cls="CeleryConfig"):
        self.config_cls = config_cls
        self.celery = None

    def register(self, app) -> Celery:
        if self.celery is not None:
            return self.celery
        config = app.config_loader.get(self.config_cls, None)
        if not config:
            raise RuntimeError(f"{self.config_cls} not found!")

        self.celery = Celery(__name__, broker=config.broker_url)
        self.celery.conf.update(asdict(config))
        return self.celery


celery_plugin = CeleryPlugin()


def register(app):
    celery_plugin.register(app)
