from fastapi import APIRouter, Request, status, Depends, HTTPException
from src.models.models import MembersModel
import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.user.crud as user_crud
from src.handler.auth import auth_manager

router = APIRouter()


@router.post('/create')
def add_user_to_collection(request: Request, member: MembersModel, logged_in_user=Depends(auth_manager)):
    # Check if user exists
    user = user_crud.find_by_username(member.user_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User does not exist')
    # Check if collection exists
    collection = collection_crud.find_by_id(member.collection_id)
    if not collection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Collection does not exist')
    # Check if logged in user is a member of the collection
    has_rights = member_crud.find_by_user_name_and_collection_id(
        logged_in_user.name, member.collection_id)
    if not has_rights:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='You are not a member of this collection')
    # Check if the user is already a member of the collection
    exists = member_crud.find_by_user_name_and_collection_id(
        member.user_name, member.collection_id)
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User is already a member of this collection')
    return member_crud.create(member)
