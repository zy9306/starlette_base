import logging
from copy import deepcopy

from tortoise import fields, models
from tortoise.contrib.starlette import register_tortoise
from tortoise.indexes import Index

DEFAULT_DB_CONFIG = {
    "connections": {
        "sqlite": "sqlite://:memory:",
        "mysql": "mysql://username:password@localhost:3306/db?minsize=2&maxsize=10",
    },
    "apps": {
        "models": {
            "models": ["your_app.models"],
            "default_connection": "mysql",
        }
    },
    "use_tz": True,
    "timezone": "UTC",
    "generate_schemas": True,
}


class TortoisePlugin:
    def __init__(self, config_name="DB_CONFIG"):
        self._config_name = config_name
        self._initialized = False

    def register(self, app):
        if self._initialized:
            return
        config = app.config_loader.get(self._config_name, None)
        if not config:
            raise RuntimeError("database config not found!")
        if missing := (set(DEFAULT_DB_CONFIG.keys()) - set(config.keys())):
            raise RuntimeError(f"database config invalid! missing keys: {missing}")
        config = deepcopy(config)
        generator_schemas = config.pop("generate_schemas", False)
        register_tortoise(app, config=config, generate_schemas=generator_schemas)
        self._initialized = True
        logging.warning("--- Tortoise ORM initialized.")


class UniqueIndex(Index):
    INDEX_TYPE = "UNIQUE"


class BaseModel(models.Model):
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
