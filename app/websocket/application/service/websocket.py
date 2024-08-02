from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from app.auth.application.exception import DecodeTokenException
from core.helpers.token import (
    TokenHelper,
    DecodeTokenException as JwtDecodeTokenException,
    ExpiredTokenException as JwtExpiredTokenException,
    MissingTokenException as JwtMissingTokenException
)
# from app.container import Container
from app.auth.application.service.jwt import JwtService


class WebSocketService:
    def __init__(self) -> None:
        self.jwt_service = JwtService()     

    async def authenticate(self, websocket: WebSocket) -> None:
        
        token = None

        # Extract the bearer token from the Sec-WebSocket-Protocol header
        protocols = websocket.headers.get("Sec-WebSocket-Protocol", "").split(", ")
        bearer_protocol = next((p for p in protocols if p.startswith("bearer.")), None)
        
        if bearer_protocol:
            token = bearer_protocol.split(".", 1)[1]

        # If not found in subprotocols, try to get token from headers
        if not token:
            auth_header = websocket.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            await websocket.close(code=4001, reason="No authentication provided")
            raise JwtMissingTokenException("No JWT token found in protocols or headers")
            
        try:
            await self.jwt_service.verify_token(token)
            await websocket.accept(subprotocol=bearer_protocol)
        except (DecodeTokenException, JwtDecodeTokenException, JwtExpiredTokenException):
            await websocket.close(code=4002, reason="Invalid token")
            raise DecodeTokenException("Invalid token")
    
    async def handle_connection(self, websocket: WebSocket) -> None:
        await self.authenticate(websocket)
        await websocket.send_text("Client connected.")

        try:
            while True:
                msg = await websocket.receive_text()
                if msg.lower() == "close":
                    await websocket.close()
                    break
                else:
                    print(f'CLIENT says - {msg}')
                    await websocket.send_text(f"Your message was: {msg}")
        except (WebSocketDisconnect, ConnectionClosed):
            print("Client disconnected")