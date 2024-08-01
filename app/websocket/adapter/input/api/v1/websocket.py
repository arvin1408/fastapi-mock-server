from fastapi import WebSocket, APIRouter, FastAPI
from app.container import Container
from app.auth.application.exception import DecodeTokenException
from core.helpers.token import (
    TokenHelper,
    DecodeTokenException as JwtDecodeTokenException,
    ExpiredTokenException as JwtExpiredTokenException,
)

websocket_router = APIRouter()

@websocket_router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):

    # Extract the token from the WebSocket's headers
    auth_header = websocket.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        await websocket.close(code=4001, reason="Invalid Authorization header")
        return

    token = auth_header.split(' ')[1]
    
    # Verify the token
    jwt_service = Container.jwt_service()
    await jwt_service.verify_token(token)

    # Handle the authenticated connection
    websocket_service = Container.websocket_service()
    await websocket_service.handle_connection(websocket)