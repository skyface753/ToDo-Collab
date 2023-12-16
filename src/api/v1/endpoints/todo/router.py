from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from src.models.models import TodoModel
from src.handler.websocket import manager
import src.api.v1.endpoints.todo.crud as todo_crud
import json
from src.handler.auth import manager as auth_manager
router = APIRouter()


@router.websocket("/ws/{collection_id}")
async def websocket_endpoint(websocket: WebSocket, collection_id: str,
                             token: str = Query(...)):
    user = await auth_manager.get_current_user(token)
    await manager.connect(websocket, user.id, collection_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            as_json = json.loads(data)
            as_json["collection_id"] = collection_id
            as_json["user_id"] = user.id
            new_todo = TodoModel(**as_json)
            created_todo = todo_crud.create(new_todo)
            created_todo = created_todo.model_dump_json(by_alias=True)
            print(created_todo)
            await manager.broadcast(created_todo, collection_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{user.id} left the chat", collection_id)


@router.post("/create")
async def create_todo(todo: TodoModel, user=Depends(auth_manager)):
    todo.user_id = user.id
    created_todo = todo_crud.create(todo)
    created_todo = created_todo.model_dump_json(by_alias=True)
    await manager.broadcast(created_todo, todo.collection_id)
    return created_todo
