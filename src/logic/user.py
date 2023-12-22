from src.models.models import UserModel
import src.api.v1.endpoints.user.crud as user_crud
import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.todo.crud as todo_crud
from fastapi import Response


def delete_user_cascade(user: UserModel):
    user_crud.delete_by_name(user.name)
    deleted_members = member_crud.delete_by_user_name(user.name)
    for member in deleted_members:
        has_members = member_crud.find_by_collection_id(member.collection_id)
        if not has_members:
            collection_crud.delete_by_id(member.collection_id)
            todo_crud.delete_by_collection_id(member.collection_id)
    todo_crud.delete_by_user_name(user.name)


def logout(response: Response):
    response.delete_cookie('access-token')
    return response
