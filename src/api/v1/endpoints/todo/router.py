from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.models.models import TodoModel
from src.handler.websocket import manager
from src.api.v1.endpoints.todo.crud import create_todo
import json

router = APIRouter()



from bson import json_util


@router.websocket("/ws/{client_id}/{team_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, team_id: str):
    await manager.connect(websocket, client_id, team_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            as_json = json.loads(data)
            as_json["team_id"] = team_id
            as_json["user_id"] = client_id
            data = json.dumps(as_json) # Back to string, to be parsed by the model
            new_todo = TodoModel.model_validate_json(data)
            created_todo = await create_todo(new_todo)
            created_todo = json_util.dumps(created_todo)
            await manager.broadcast(created_todo, team_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", team_id)
