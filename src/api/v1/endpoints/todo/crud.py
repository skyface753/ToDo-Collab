from src.models.models import TodoModel, CreateTodoModel
from typing import List
from src.config.scylla import session
from src.api.v1.endpoints.collection.crud import refresh_updated_at_by_id as refresh_collection_updated_at_by_id
import uuid


def create_table():
    session.execute(
        """CREATE TABLE IF NOT EXISTS todos
        (id uuid PRIMARY KEY, title text, description text,
        user_name text, collection_id uuid, created_at timestamp, updated_at timestamp)
        """)
    session.execute(
        'CREATE INDEX IF NOT EXISTS user_name_index ON todos (user_name)')
    session.execute(
        'CREATE INDEX IF NOT EXISTS collection_id_index ON todos (collection_id)')


create_table()


def todo_model_from_row(row):
    return TodoModel(id=row.id, title=row.title,
                     description=row.description, user_name=row.user_name,
                     collection_id=row.collection_id, created_at=row.created_at,
                     updated_at=row.updated_at)


def create(new_todo: CreateTodoModel) -> TodoModel:
    """
    Insert a new todo record.

    A unique `id` will be created and provided in the response.
    """
    new_id = uuid.uuid4()
    session.execute(
        """
        INSERT INTO todos (id, title, description, user_name, collection_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, toTimestamp(now()), toTimestamp(now()))
        """,
        (new_id, new_todo.title, new_todo.description, new_todo.user_name, new_todo.collection_id))
    refresh_collection_updated_at_by_id(new_todo.collection_id)
    todo = find_by_id(str(new_id))
    return todo


def find_by_collection_id(collection_id: str) -> List[TodoModel]:
    """
    Get all todos for a collection.
    """
    todos = []
    results = session.execute(
        'SELECT * FROM todos WHERE collection_id = %s', (uuid.UUID(str(collection_id)),))
    for row in results:
        todos.append(todo_model_from_row(row))
    todos.sort(key=lambda x: x.updated_at, reverse=True)
    return todos


def find_by_user_name(user_name: str) -> List[TodoModel]:
    """
    Get all todos for a user.
    """
    todos = []
    results = session.execute(
        'SELECT * FROM todos WHERE user_name = %s', (user_name,))
    for row in results:
        todos.append(todo_model_from_row(row))
    todos.sort(key=lambda x: x.updated_at, reverse=True)
    return todos


def delete_by_id(id: str) -> None:
    """
    Delete a todo by its unique id.
    """
    session.execute('DELETE FROM todos WHERE id = %s', (id,))


def find_by_id(id: str) -> TodoModel or None:
    """
    Find a todo by its unique id.
    """
    results = session.execute(
        'SELECT * FROM todos WHERE id = %s', (uuid.UUID(str(id)),))
    for row in results:
        return todo_model_from_row(row)
    return None


def find_all() -> List[TodoModel]:
    """
    Find all todos.
    """
    todos = []
    results = session.execute('SELECT * FROM todos')
    for row in results:
        todos.append(todo_model_from_row(row))
    todos.sort(key=lambda x: x.updated_at, reverse=True)
    return todos


def delete_by_collection_id(collection_id: str) -> None:
    """
    Delete all todos for a collection.
    """
    todos = find_by_collection_id(collection_id)
    for todo in todos:
        delete_by_id(todo.id)


def delete_by_user_name(user_name: str) -> None:
    """
    Delete all todos for a user.
    """
    todos = find_by_user_name(user_name)
    for todo in todos:
        delete_by_id(todo.id)
