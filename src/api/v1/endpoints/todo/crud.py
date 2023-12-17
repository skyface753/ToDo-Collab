from src.models.models import TodoModel
from src.config.env import todo_collection
from typing import List
from bson.objectid import ObjectId


def create(new_todo: TodoModel) -> TodoModel:
    """
    Insert a new todo record.

    A unique `id` will be created and provided in the response.
    """
    new_todo = todo_collection.insert_one(
        new_todo.model_dump(by_alias=True, exclude=['id']),
    )
    # Add the user name and team name to the response
    created_todo = todo_collection.find_one({'_id': new_todo.inserted_id})
    return TodoModel(**created_todo)


def find_by_collection_id(collection_id: str) -> List[TodoModel]:
    """
    Get all todos for a collection.
    """
    todos = []
    for todo in todo_collection.find({'collection_id': collection_id}):
        todos.append(TodoModel(**todo))
    return todos


def delete_by_id(id: str) -> None:
    """
    Delete a todo by its unique id.
    """
    todo_collection.delete_one({'_id': ObjectId(id)})


def find_by_id(id: str) -> TodoModel or None:
    """
    Find a todo by its unique id.
    """
    todo = todo_collection.find_one({'_id': ObjectId(id)})
    if todo is None:
        return None
    return TodoModel(**todo)


def find_all() -> List[TodoModel]:
    """
    Find all todos.
    """
    todos = []
    for todo in todo_collection.find():
        todos.append(TodoModel(**todo))
    return todos


def delete_by_collection_id(collection_id: str) -> None:
    """
    Delete all todos for a collection.
    """
    todo_collection.delete_many({'collection_id': collection_id})


def delete_by_user_id(user_id: str) -> None:
    """
    Delete all todos for a user.
    """
    todo_collection.delete_many({'user_id': user_id})
