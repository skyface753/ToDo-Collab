import src.api.v1.endpoints.todo.crud as todo_crud
import src.api.v1.endpoints.user.crud as user_crud
import src.api.v1.endpoints.collection.crud as collection_crud
from src.models.models import CreateTodoModel


def test_todo_create_read_update_delete():
    # Mock a user and collection
    user_name = 'test_user'
    user_password = 'test_password'
    user = user_crud.create(user_crud.UserModel(
        name=user_name, password=user_password))
    collection_name = 'test_collection'
    collection = collection_crud.create(
        collection_crud.CreateCollectionModel(name=collection_name))
    # Create a todo

    todo_title = 'test_todo'
    todo_description = 'test_description'
    todo = CreateTodoModel(title=todo_title, description=todo_description, user_name=user.name,
                           collection_id=collection.id)
    number_of_todos = len(todo_crud.find_all())
    todo = todo_crud.create(todo)
    created_todo = todo_crud.find_by_id(todo.id)
    assert created_todo.title == todo_title
    assert created_todo.description == todo_description
    assert created_todo.user_name == user.name
    assert created_todo.collection_id == collection.id
    # Find by collection_id
    found_todos = todo_crud.find_by_collection_id(collection.id)
    assert len(found_todos) == 1
    assert found_todos[0].title == todo_title
    assert found_todos[0].description == todo_description
    assert found_todos[0].user_name == user.name
    assert found_todos[0].collection_id == collection.id
    assert found_todos[0].id == todo.id
    assert number_of_todos + 1 == len(todo_crud.find_all())

    # Delete
    todo_crud.delete_by_id(todo.id)
    assert todo_crud.find_by_id(todo.id) is None
    assert len(todo_crud.find_all()) == 0
    assert len(todo_crud.find_by_collection_id(collection.id)) == 0
    user_crud.delete_by_name(user.name)
    collection_crud.delete_by_id(collection.id)
