import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.user.crud as user_crud

import src.api.v1.endpoints.member.crud as member_crud

from src.models.models import UserModel, MembersModel, CreateCollectionModel

import uuid


def test_member_create_read_update_delete():
    fake_uuid = uuid.uuid4()
    # Arrange create collection and user
    user_name = 'test_user'
    user_password = 'test_password'
    user = UserModel(name=user_name, password=user_password)
    created_user = user_crud.create(user)
    assert created_user.name == user_name
    assert created_user.password != user_password

    collection_name = 'test_collection'
    collection = CreateCollectionModel(name=collection_name)
    created_collection = collection_crud.create(collection)
    assert created_collection.name == collection_name
    assert created_collection.id is not None
    collection_id = created_collection.id

    # Act
    number_of_members = len(member_crud.find_all())
    member = MembersModel(user_name=user_name,
                          collection_id=collection_id)
    created_member = member_crud.create(member)
    assert created_member.user_name == user_name
    assert created_member.collection_id == collection_id

    # Assert
    assert len(member_crud.find_all()) == number_of_members + 1
    found_member = member_crud.find_by_user_name_and_collection_id(
        created_member.user_name, created_member.collection_id)

    assert found_member.user_name == created_user.name
    assert found_member.collection_id == created_collection.id

    # Act: find by user_name
    found_members = member_crud.find_by_user_name(user_name)
    assert len(found_members) == 1
    assert found_members[0].user_name == user_name
    assert found_members[0].collection_id == created_collection.id

    # Act: find by collection_id
    found_members = member_crud.find_by_collection_id(collection_id)
    assert len(found_members) == 1
    assert found_members[0].user_name == user_name
    assert found_members[0].collection_id == created_collection.id

    # Act: find by user_name, collection_id

    found_member = member_crud.find_by_user_name_and_collection_id(
        user_name, collection_id)
    assert found_member.user_name == created_user.name
    assert found_member.collection_id == created_collection.id

    # Found by user_name, collection_id not in db
    found_not_existing_member = member_crud.find_by_user_name_and_collection_id(
        user_name, fake_uuid)
    assert found_not_existing_member is None
    found_not_existing_member = member_crud.find_by_user_name_and_collection_id(
        'fake_user', collection_id)
    assert found_not_existing_member is None

    # Act: delete
    member_crud.delete_by_user_name_and_collection_id(
        user_name, collection_id)

    assert len(member_crud.find_all()) == number_of_members
    assert member_crud.find_by_user_name_and_collection_id(
        user_name, collection_id) is None

    user_crud.delete_by_name(user_name)
    collection_crud.delete_by_id(collection_id)
    assert user_crud.find_by_username(user_name) is None
    assert collection_crud.find_by_id(collection_id) is None
    assert len(member_crud.find_all()) == number_of_members
    assert member_crud.find_by_user_name_and_collection_id(
        user_name, collection_id) is None
