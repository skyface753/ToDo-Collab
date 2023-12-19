from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import src.api.v1.endpoints.todo.crud as todo_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.logic.collection as collection_logic
from src.handler.auth import auth_manager
from src.config.templates import templates
from src.config.env import USE_WSS

router = APIRouter()


@router.get('/', response_class=HTMLResponse, name='collections')
def get_my_collections(request: Request, user=Depends(auth_manager)):
    collections = collection_logic.find_collections_for_user(user.name)
    return templates.TemplateResponse('collections.html.jinja2',
                                      {'request': request,
                                       'collections': collections,
                                       'user': user})


@router.get('/{collection_id}', response_class=HTMLResponse, name='collection')
async def get_collection(request: Request, collection_id: str,
                         user=Depends(auth_manager)):
    token = await auth_manager._get_token(request)
    if user:
        collection = collection_crud.find_by_id(collection_id)
        todos = todo_crud.find_by_collection_id(collection_id)
        todos_json = []
        for todo in todos:
            todos_json.append(todo.model_dump_json(by_alias=True))
        websocket_url = str(request.url_for(
            'ws', collection_id=collection_id).include_query_params(token=token))
        # Use wss
        if USE_WSS:
            websocket_url = websocket_url.replace('ws://', 'wss://')
        return templates.TemplateResponse('collection.html.jinja2',
                                          {'request': request,
                                           'collection': collection,
                                           'user': user,
                                           'token': token,
                                           'websocket_url': websocket_url,
                                           'todossosos': todos_json})
    else:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
