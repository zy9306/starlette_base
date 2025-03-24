from typing import Callable

from starlette.applications import Starlette

from .plugins.base import PluginManager
from .route import RouteManager


class StarletteBaseApp(Starlette):
    def __init__(self, config_loader=None, routes=None, middleware: Callable[[Starlette], list] | list = None):
        self.config_loader = config_loader

        if callable(middleware):
            middleware = middleware(self)

        super().__init__(
            debug=self.config_loader.AppConfig.debug,
            routes=routes or RouteManager.routes,
            middleware=middleware or [],
        )

        self.plugin_manager = PluginManager(self)
        if plugins := self.config_loader.AppConfig.plugins:
            self.plugin_manager.register_plugins(plugins)
