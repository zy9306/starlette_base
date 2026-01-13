from typing import Callable

from starlette.applications import Starlette


class StarletteBaseApp(Starlette):
    def __init__(self, config_loader=None, routes=None, middleware: Callable[[Starlette], list] | list = None):
        self.config_loader = config_loader

        if callable(middleware):
            middleware = middleware(self)

        super().__init__(
            debug=self.config_loader.APP_CONFIG["debug"],
            routes=routes or [],
            middleware=middleware or [],
        )
