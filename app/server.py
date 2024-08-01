from fastapi import Depends, FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from websockets.exceptions import ConnectionClosed

from app.auth.adapter.input.api import router as auth_router
from app.container import Container
from app.user.adapter.input.api import router as user_router
from app.websocket.adapter.input.api import router as websocket_router
from app.websocket.adapter.input.api.v1.socketio import NoPrefixNamespace

from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLogMiddleware,
    SQLAlchemyMiddleware,
)
from core.helpers.cache import Cache, CustomKeyMaker, RedisBackend
from core.socketio.socketio import sio
import socketio


def init_routers(app_: FastAPI) -> None:
    container = Container()
    user_router.container = container
    auth_router.container = container
    websocket_router.container = container
    app_.include_router(user_router)
    app_.include_router(auth_router)
    app_.include_router(websocket_router)    


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLogMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())

# TO DEBUG
def init_socketio(app_: FastAPI) -> None:
    socketio_server = sio.register_namespace(NoPrefixNamespace("/"))
    sio_asgi_app = socketio.ASGIApp(socketio_server=socketio_server, other_asgi_app=app_)
    app_.add_route("/api/v1/io", route=sio_asgi_app, methods=["GET", "POST"])
    app_.add_websocket_route("/api/v1/io", sio_asgi_app)


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Mock FastAPI Server",
        description="Mock server for REST API and Websocket connection tests",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    # init_socketio(app_=app_)
    # app_.mount("/app/app/static", StaticFiles(directory="/app/app/static"), name="static")

    return app_


app = create_app()

@app.get("/")
async def root():
    return {"message": "Connected to server successfully!"}
