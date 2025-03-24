from starlette.routing import Route


class RouteManager:
    routes = []

    @classmethod
    def add_route(cls, path: str, endpoint, methods: list = ["GET"]):
        for route in cls.routes:
            if route.path == path and set(route.methods) == set(methods):
                raise ValueError(f"Route for {path} with methods {methods} already exists.")

        cls.routes.append(Route(path, endpoint, methods=methods))

    @classmethod
    def get_routes(cls):
        return cls.routes

    @classmethod
    def register(cls, path: str, methods: list = ["GET"]):
        def decorator(func):
            cls.add_route(path, func, methods)
            return func

        return decorator
