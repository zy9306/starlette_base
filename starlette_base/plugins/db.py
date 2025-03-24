from dataclasses import asdict, dataclass

from starlette.config import Config
from tortoise.contrib.starlette import register_tortoise

config = Config()


@dataclass
class DBConfig:
    connections: dict
    apps: dict
    use_tz: bool
    timezone: str
    generate_schemas: bool

    def __init__(self, connections=None, apps=None, use_tz=True, timezone="UTC", generate_schemas=True):
        self.connections = connections or {
            "sqlite": "sqlite://:memory:",
            "mysql": "mysql://username:password@localhost:3306/db?minsize=2&maxsize=10",
        }
        self.apps = apps or {
            "models": {
                "models": ["your_app.models"],
                "default_connection": "mysql",
            }
        }
        self.use_tz = use_tz
        self.timezone = timezone
        self.generate_schemas = generate_schemas


def register(app):
    db_config = asdict(app.config_loader.DBConfig)
    generator_schemas = db_config.pop("generate_schemas", False)
    register_tortoise(app, config=db_config, generate_schemas=generator_schemas)
