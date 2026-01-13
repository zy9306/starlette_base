import importlib
import logging
import os
from threading import Lock


class ConfigLoader(dict):
    _instance = None
    _lock = Lock()

    def __new__(cls, configs_package, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._load_configs(configs_package)
        return cls._instance

    def _load_configs(self, configs_package="configs"):
        if not getattr(self, "_is_loaded", False):
            env = os.environ.get("ENV", "development")
            configs_module = importlib.import_module(f"{configs_package}.{env}")
            logging.warning(f"Loading configs from {configs_module.__name__}")
            for attribute_name in dir(configs_module):
                attr = getattr(configs_module, attribute_name)
                setattr(self, attribute_name, attr)
                self[attribute_name] = attr
            self._is_loaded = True
