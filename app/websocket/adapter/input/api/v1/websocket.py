from fastapi import WebSocket, APIRouter, FastAPI
from app.container import Container

websocket_router = APIRouter()

@websocket_router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    websocket_service = Container.websocket_service()
    await websocket_service.handle_connection(websocket)