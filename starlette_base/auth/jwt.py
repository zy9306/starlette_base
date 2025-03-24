from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection
from tortoise.models import Model

from ..middlewares.jwt import JWTPayload as JWTPayload


class JWTAuthenticationBackend(AuthenticationBackend):
    async def auth(self, jwt_payload: JWTPayload | None) -> tuple[AuthCredentials, Model]:
        raise NotImplementedError

    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, Model] | None:
        jwt_payload: JWTPayload = conn.scope.get("jwt_payload")
        return await self.auth(jwt_payload)
