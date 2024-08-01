import socketio
from core.socketio.socketio import sio
# from app.container import Container

class NoPrefixNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print("connect ", sid)

        # Extract the token from the WebSocket's headers
        # headers = environ.get('HTTP_AUTHORIZATION')
        # if not headers or not headers.startswith('Bearer '):
        #     await self.sio.disconnect(sid)
        #     return

        # token = headers.split(' ')[1]
        
        # # Verify the token
        # jwt_service = Container.jwt_service()
        # try:
        #     await jwt_service.verify_token(token)
        # except Exception as e:
        #     await self.sio.disconnect(sid)
        #     return        

    async def on_message(self, sid, data):
        print("message ", data)
        await sio.emit("response", "hi " + data)

    def on_disconnect(self, sid):
        print("disconnect ", sid)

# socketio_server = sio.register_namespace(NoPrefixNamespace("/"))
