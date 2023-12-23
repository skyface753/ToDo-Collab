from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from src.handler.auth import auth_manager
import src.logic.collection as collection_logic
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.todo.crud as todo_crud
from src.models.models import CollectionModel, CreateCollectionModel, CollectionModelWithTodos
from src.config.env import USE_WSS
from typing import List

router = APIRouter()


@router.get('', response_model=List[CollectionModel], name='get_collections')
def get_collections(user=Depends(auth_manager)):
    collections = collection_logic.find_collections_for_user(user.name)
    return collections


@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=CollectionModel, name='create_collection')
def create_collection(collection: CreateCollectionModel, user=Depends(auth_manager)):
    # Trim the name
    collection.name = collection.name.strip()
    if collection.name == '' or collection.name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Name cannot be empty')
    collection = collection_logic.create_collection_for_user(collection, user)
    data = collection.model_dump_json(by_alias=True)
    return Response(content=(data), media_type='application/json',
                    status_code=status.HTTP_201_CREATED)


@router.get('/{collection_id}', response_model=CollectionModelWithTodos, name='get_collection')
async def get_collection(request: Request, collection_id: str,
                         generate_websocket_url: bool = False, user=Depends(auth_manager)):
    collection = collection_crud.find_by_id(collection_id)
    if collection is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Collection not found')
    is_member = member_crud.find_by_user_name_and_collection_id(
        user.name, collection_id)
    if not is_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is not a member of this collection')
    todos = todo_crud.find_by_collection_id(collection_id)
    # Order todos by creation date 2023-12-23 08:36:38.766000
    todos.sort(key=lambda x: x.created_at)
    collection_response = CollectionModelWithTodos(
        **collection.model_dump(), todos=todos)
    token = await auth_manager._get_token(request)
    if generate_websocket_url:
        websocket_url = str(request.url_for(
            'ws', collection_id=collection_id).include_query_params(token=token))
        # Use wss
        if USE_WSS:
            websocket_url = websocket_url.replace('ws://', 'wss://')
        collection_response.websocket_url = websocket_url
    return collection_response.model_dump(by_alias=True)


@router.delete('/{collection_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(collection_id: str, user=Depends(auth_manager)):
    is_member = member_crud.find_by_user_name_and_collection_id(
        user.name, collection_id)
    if not is_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is not a member of this collection')
    collection_crud.delete_by_id(collection_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
