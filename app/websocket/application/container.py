from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.websocket.application.service.websocket import WebSocketService

class WebsocketContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    websocket_service = Factory(WebSocketService)    

