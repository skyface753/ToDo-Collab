from fastapi import APIRouter, Depends, status, Response, HTTPException
from src.handler.auth import auth_manager
import src.logic.collection as collection_logic
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.member.crud as member_crud
from src.models.models import CollectionModel, CreateCollectionModel, CollectionModelWithTodos
from typing import List

router = APIRouter()


@router.get('', response_model=List[CollectionModelWithTodos])
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


@router.get('/{collection_id}', response_model=CollectionModel, name='get_collection')
def get_collection(collection_id: str, user=Depends(auth_manager)):
    collection = collection_crud.find_by_id(collection_id)
    return collection.model_dump(by_alias=True)


@router.delete('/{collection_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(collection_id: str, user=Depends(auth_manager)):
    is_member = member_crud.find_by_user_name_and_collection_id(
        user.name, collection_id)
    if not is_member:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User is not a member of this collection')
    collection_crud.delete_by_id(collection_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
