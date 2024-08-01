from .authentication import AuthenticationMiddleware, AuthBackend
from .response_log import ResponseLogMiddleware
from .sqlalchemy import SQLAlchemyMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class CSPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'self' ws: wss:;"
        return response
    
__all__ = [
    "AuthenticationMiddleware",
    "AuthBackend",
    "SQLAlchemyMiddleware",
    "ResponseLogMiddleware",
    "CSPMiddleware"
]
