# from bson import json_util
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from src.models.models import TodoModel
from src.handler.websocket import manager
from src.api.v1.endpoints.todo.crud import create_todo
import json
from src.handler.auth import manager as auth_manager
from src.models.models import UserModel
import json
router = APIRouter()


@router.websocket("/ws/{collection_id}")
async def websocket_endpoint(websocket: WebSocket, collection_id: str, token: str = Query(...)):
    user = await auth_manager.get_current_user(token)
    # user = UserModel(**user)
    # user = json.loads(json.dumps(user, default=lambda o: str(o)))
    print(user.id)
    # user_id = user["_id"]

    await manager.connect(websocket, user.id, collection_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            as_json = json.loads(data)
            as_json["collection_id"] = collection_id
            as_json["user_id"] = user.id
            new_todo = TodoModel(**as_json)
            created_todo = await create_todo(new_todo)
            created_todo = created_todo.model_dump_json(by_alias=True)
            print(created_todo)
            await manager.broadcast(created_todo, collection_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{user.id} left the chat", collection_id)
