from starlette.routing import Route


class RouteManager:
    def __init__(self, prefix: str = ""):
        self.routes = []
        self.prefix = prefix

    def add_route(self, path: str, endpoint, methods: list = ["GET"]):
        for route in self.routes:
            if route.path == path and set(route.methods) == set(methods):
                raise ValueError(f"Route for {path} with methods {methods} already exists.")

        self.routes.append(Route(f"{self.prefix}{path}", endpoint, methods=methods))

    def get_routes(self):
        return self.routes

    def register(self, path: str, methods: list = ["GET"]):
        def decorator(func):
            self.add_route(path, func, methods)
            return func

        return decorator
