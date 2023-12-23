import src.api.v1.endpoints.user.crud as user_crud
from src.models.models import UserModel


def test_user_create_read_update_delete():
    username = 'test_user'
    password = 'test_password'
    user = UserModel(name=username, password=password)
    number_of_users = len(user_crud.find_all())
    created_user = user_crud.create(user)
    assert created_user is not None
    assert created_user.name == username
    assert created_user.password != password
    assert created_user.password != 'test_password'
    new_length = len(user_crud.find_all())
    assert new_length == number_of_users + 1
    user_by_username = user_crud.find_by_username(username)
    assert created_user.name == user_by_username.name
    assert created_user.password == user_by_username.password
    serialized_user = created_user.model_dump(by_alias=True)
    assert serialized_user['password'] != password
    # should be *****
    assert serialized_user['password'] == '********'
    # find by not existing username
    assert user_crud.find_by_username('not_existing_username') is None

    # Delete the user
    user_crud.delete_by_name(username)
    assert len(user_crud.find_all()) == number_of_users
