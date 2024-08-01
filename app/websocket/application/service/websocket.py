from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed


class WebSocketService:
    async def handle_connection(self, websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            await websocket.send_text("Connection established!")
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