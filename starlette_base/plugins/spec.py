import logging

from spectree import SpecTree


class SpecTreePlugin:
    def __init__(self, config_name="SPECTREE_CONFIG"):
        self._config_name = config_name
        self._spec = SpecTree("starlette")
        self._initialized = False

    def register(self, app):
        if self._initialized:
            return self._spec
        self._spec.register(app)
        self._initialized = True
        logging.warning("--- SpecTree initialized.")
        return self._spec

    @property
    def spec(self) -> SpecTree:
        return self._spec
