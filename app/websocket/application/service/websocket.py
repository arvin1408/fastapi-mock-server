from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from app.auth.application.exception import DecodeTokenException
from core.helpers.token import (
    TokenHelper,
    DecodeTokenException as JwtDecodeTokenException,
    ExpiredTokenException as JwtExpiredTokenException,
)
# from app.container import Container
from app.auth.application.service.jwt import JwtService


class WebSocketService:
    def __init__(self) -> None:
        self.jwt_service = JwtService()     

    async def authenticate(self, websocket: WebSocket) -> None:
        await websocket.accept()
        
        # Extract the token from the WebSocket's subprotocols
        protocols = websocket.scope.get('subprotocols', [])
        if len(protocols) != 1:
            await websocket.close(code=4001, reason="Invalid protocol")
            return

        token = protocols[0]

        try:
            await self.jwt_service.verify_token(token)
        except (DecodeTokenException, JwtDecodeTokenException, JwtExpiredTokenException):
            print(f'Invalid token: {token}')
            await websocket.close(code=4002, reason="Invalid token")
            return
    
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