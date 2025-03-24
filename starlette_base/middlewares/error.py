from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

from ..exceptions import HTTPError


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPError as e:
            return JSONResponse({"message": e.message}, status_code=e.status_code)
        except DoesNotExist as e:
            return JSONResponse({"message": str(e)}, status_code=404)
        except IntegrityError as e:
            return JSONResponse({"message": str(e)}, status_code=400)
