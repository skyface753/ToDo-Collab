from src.models.models import UserModel, MembersModel, CreateCollectionModel, TodoModel
import src.api.v1.endpoints.user.crud as user_crud
import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.todo.crud as todo_crud
import src.logic.user as user_logic
import src.logic.collection as collection_logic


def test_collection_create_delete_cascade():
    """
    Test a whole cascade of collection creation and deletion
    A user is created, a collection is created for that user,
        a todo is created for that user and collection
    Then the user is deleted, and the collection and todo should be deleted as well
    """
    # First User + Collection
    user_name = 'test_user'
    user_password = 'test_password'
    collection_name = 'test_collection'
    user = UserModel(name=user_name, password=user_password)
    created_user = user_crud.create(user)
    collection = CreateCollectionModel(name=collection_name)
    collection = collection_logic.create_collection_for_user(
        collection, created_user)  # This also creates a member
    todo_title = 'test_todo'
    todo_description = 'test_description'
    todo = TodoModel(title=todo_title, description=todo_description,
                     user_id=created_user.id, collection_id=collection.id)
    todo = todo_crud.create(todo)

    # Second User + Collection
    user_name2 = 'test_user2'
    user_password2 = 'test_password2'
    collection_name2 = 'test_collection2'
    user2 = UserModel(name=user_name2, password=user_password2)
    created_user2 = user_crud.create(user2)
    collection2 = CreateCollectionModel(name=collection_name2)
    collection2 = collection_logic.create_collection_for_user(
        collection2, created_user2)  # This also creates a member
    todo_title2 = 'test_todo2'
    todo_description2 = 'test_description2'
    todo2 = TodoModel(title=todo_title2, description=todo_description2,
                      user_id=created_user2.id, collection_id=collection2.id)
    todo2 = todo_crud.create(todo2)

    # 3rd Todo for second user in first collection
    todo_title3 = 'test_todo3'
    todo_description3 = 'test_description3'
    todo3 = TodoModel(title=todo_title3, description=todo_description3,
                      user_id=created_user2.id, collection_id=collection.id)
    todo3 = todo_crud.create(todo3)

    # Add second user to first collection
    member = MembersModel(user_id=created_user2.id,
                          collection_id=collection.id)
    member_crud.create(member)

    number_of_collections_1 = len(
        collection_logic.find_collections_for_user(created_user.id))
    number_of_collections_2 = len(
        collection_logic.find_collections_for_user(created_user2.id))
    number_of_todos_1 = len(todo_crud.find_by_collection_id(collection.id))
    number_of_todos_2 = len(todo_crud.find_by_collection_id(collection2.id))
    assert number_of_collections_1 == 1
    assert number_of_collections_2 == 2
    assert number_of_todos_1 == 2
    assert number_of_todos_2 == 1

    # Delete first user
    user_logic.delete_user_cascade(created_user)
    assert user_crud.find_by_id(created_user.id) is None
    assert len(user_crud.find_all()) == 1
    assert user_crud.find_by_id(created_user2.id) is not None
    assert len(user_crud.find_all()) == 1
    assert len(collection_logic.find_collections_for_user(created_user.id)) == 0
    assert len(collection_logic.find_collections_for_user(
        created_user2.id)) == 2
    assert len(member_crud.find_by_user_id(created_user.id)) == 0
    assert len(member_crud.find_by_user_id(created_user2.id)) == 2
    assert len(todo_crud.find_all()) == 2
    assert len(todo_crud.find_by_collection_id(collection.id)) == 1
    assert len(todo_crud.find_by_collection_id(collection2.id)) == 1

    # Delete second user
    user_logic.delete_user_cascade(created_user2)
    assert user_crud.find_by_id(created_user2.id) is None
    assert len(user_crud.find_all()) == 0
    assert len(collection_logic.find_collections_for_user(
        created_user2.id)) == 0
    assert len(member_crud.find_by_user_id(created_user2.id)) == 0
    assert len(member_crud.find_by_collection_id(collection.id)) == 0
    assert len(member_crud.find_by_collection_id(collection2.id)) == 0
    assert len(collection_crud.find_all()) == 0
    assert len(todo_crud.find_all()) == 0
    assert len(member_crud.find_all()) == 0
    assert len(todo_crud.find_by_collection_id(collection.id)) == 0
    assert len(todo_crud.find_by_collection_id(collection2.id)) == 0
