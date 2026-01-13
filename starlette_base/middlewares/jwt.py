import logging
from datetime import datetime

import jwt
from pydantic import BaseModel
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Receive, Scope, Send


class JWTPayload(BaseModel):
    sub: str
    name: str | None = None
    iat: int = None
    exp: int = None
    session_id: str = None


DEFAULT_JWT_CONFIG = {
    "cookie_name": "jwt",
    "algorithm": "HS256",
    "key": "secret",
    "expiration_delta": 7 * 24 * 3600,
}


class JWTMiddleware:
    def __init__(self, app: ASGIApp, config_loader, config_name="JWT_CONFIG") -> None:
        self.app = app
        self.jwt_config = config_loader.get(config_name, None)
        if not self.jwt_config:
            raise RuntimeError(f"{config_name} not found!")
        if missing := (set(DEFAULT_JWT_CONFIG.keys()) - set(self.jwt_config.keys())):
            raise RuntimeError(f"JWT config invalid! missing keys: {missing}")
        self.jwt_payload = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return
        connection = HTTPConnection(scope)
        jwt_token = connection.cookies.get(self.jwt_config["cookie_name"])
        self.jwt_payload = self.decode_jwt(jwt_token)
        scope["jwt_payload"] = self.jwt_payload
        await self.app(scope, receive, send)

    def decode_jwt(self, jwt_token):
        if not jwt_token:
            return
        try:
            jwt_payload = jwt.decode(
                jwt=jwt_token,
                key=self.jwt_config["key"],
                algorithms=self.jwt_config["algorithm"],
            )
            return JWTPayload(**jwt_payload)
        except jwt.ExpiredSignatureError:
            logging.error("JWT token has expired", exc_info=True)
        except Exception as e:
            logging.error(e, exc_info=True)

    def encode_jwt(self, payload: JWTPayload):
        payload.iat = int(datetime.utcnow().timestamp())
        payload.exp = payload.iat + self.expiration_delta
        return jwt.encode(
            payload.model_dump(),
            key=self.jwt_config["key"],
            algorithm=self.jwt_config["algorithm"],
        )
