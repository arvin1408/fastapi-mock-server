import socketio

class SocketIOService:
    def __init__(self, sio: socketio.AsyncServer):
        self.sio = sio
        self.register_events()

    def register_events(self):
        @self.sio.event
        async def connect(sid, environ):
            await self.handle_connection(sid)

        @self.sio.event
        async def disconnect(sid):
            print("Client disconnected")

        @self.sio.event
        async def message(sid, data):
            await self.handle_message(sid, data)

    async def handle_connection(self, sid: str, environ) -> None:
       
        # Handle the authenticated connection
        print(f"Client connected: {sid}")
        await self.sio.send(sid, "Connection established!")
    
    async def handle_message(self, sid: str, msg: str) -> None:
        if msg.lower() == "close":
            await self.sio.disconnect(sid)
        else:
            print(f'CLIENT says - {msg}')
            await self.sio.send(sid, f"Your message was: {msg}")        