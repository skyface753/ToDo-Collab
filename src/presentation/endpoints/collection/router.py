from fastapi import APIRouter, Depends, status, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.models.models import CollectionModel, MembersModel
import src.api.v1.endpoints.todo.crud as todo_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.member.crud as member_crud
from src.logic.collection import find_collections_for_user
from src.handler.auth import manager as auth_manager
router = APIRouter()

templates = Jinja2Templates(directory="src/presentation/templates")


@router.get("/", response_class=HTMLResponse, name="collections")
def get_my_collection(request: Request, user=Depends(auth_manager)):
    collections = find_collections_for_user(user.id)
    return templates.TemplateResponse("collections.html.jinja2",
                                      {"request": request,
                                       "collections": collections,
                                       "user": user})


@router.post("/create")
def create_collection(request: Request, name: str = Form(...),
                      user=Depends(auth_manager)):
    user_id = user.id
    collection = CollectionModel(name=name)
    collection = collection_crud.create(collection)
    member = MembersModel(user_id=user_id, collection_id=collection.id)
    member_crud.create(member)
    url = request.url_for("collection", collection_id=collection.id)
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{collection_id}", response_class=HTMLResponse, name="collection")
async def get_collection(request: Request, collection_id: str,
                         user=Depends(auth_manager)):
    token = await auth_manager._get_token(request)
    if user:
        collection = collection_crud.find_by_id(collection_id)
        todos = todo_crud.find_by_collection_id(collection_id)
        todos_json = []
        for todo in todos:
            todos_json.append(todo.model_dump_json(by_alias=True))
        return templates.TemplateResponse("collection.html.jinja2",
                                          {"request": request,
                                           "collection": collection,
                                           "user": user,
                                           "token": token,
                                           "todossosos": todos_json})
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
