from fastapi import APIRouter, Query, Depends, HTTPException, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import src.api.v1.endpoints.todo.crud as todo_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.member.crud as member_crud
from src.logic.collection import find_collections_for_user
from src.handler.auth import manager as auth_manager
router = APIRouter()

templates = Jinja2Templates(directory="src/presentation/templates")


@router.get("/")
async def get_my_collection(request: Request, user=Depends(auth_manager)):
    collections = await find_collections_for_user(user.id)
    return templates.TemplateResponse("collections.html.jinja2", {"request": request, "collections": collections, "user": user})


@router.post("/create")
async def create_collection(name: str, user=Depends(auth_manager)):
    user_id = user.id
    collection = await collection_crud.create(name)
    await member_crud.create(user_id, collection.id)
    return collection


@router.get("/{collection_id}", response_class=HTMLResponse, name="collection")
async def get_collection(request: Request, collection_id: str, user=Depends(auth_manager)):
    token = await auth_manager._get_token(request)
    if user:
        todos = await todo_crud.find_by_collection_id(collection_id)
        todos = todos.model_dump_json(by_alias=True)
        return templates.TemplateResponse("collection.html.jinja2", {"request": request, "collection_id": collection_id, "user": user, "token": token, "todossosos": todos})
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
