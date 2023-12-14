from src.models.models import TodoModel, UserModel
from src.config.env import todo_collection, user_collection
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.user.crud as user_crud
from typing import List


async def create_todo(new_todo: TodoModel) -> TodoModel:
    """
    Insert a new todo record.

    A unique `id` will be created and provided in the response.
    """
    collection = await collection_crud.find_by_id(new_todo.collection_id)
    if collection is None:
        return None
    user = await user_crud.find_by_id(new_todo.user_id)
    if user is None:
        return None

    new_todo = await todo_collection.insert_one(
        new_todo.model_dump(by_alias=True, exclude=["id"])
    )
    # Add the user name and team name to the response
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    created_todo = TodoModel(**created_todo)
    # Add the user name and team name to the response

    created_todo.user_name = user.name
    created_todo.collection_name = collection.name

    return created_todo


async def find_by_collection_id(collection_id: str) -> List[TodoModel]:
    """
    Get all todos for a collection.
    """
    todos = await todo_collection.find({"collection_id": collection_id}).to_list(length=100)
    if todos is None:
        return None
    return [TodoModel(**t) for t in todos]
