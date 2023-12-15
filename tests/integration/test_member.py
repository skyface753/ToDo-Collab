import src.api.v1.endpoints.collection.crud as collection_crud
import src.api.v1.endpoints.user.crud as user_crud

import src.api.v1.endpoints.member.crud as member_crud

from src.models.models import CollectionModel, UserModel, MembersModel


def test_member_create_read_update_delete():
    # Arrange create collection and user
    user_name = "test_user"
    user_password = "test_password"
    user = UserModel(name=user_name, password=user_password)
    created_user = user_crud.create(user)
    assert created_user.name == user_name
    assert created_user.id is not None
    user_id = created_user.id

    collection_name = "test_collection"
    collection = CollectionModel(name=collection_name)
    created_collection = collection_crud.create(collection)
    assert created_collection.name == collection_name
    assert created_collection.id is not None
    collection_id = created_collection.id

    # Act
    number_of_members = len(member_crud.find_all())
    member = MembersModel(user_id=user_id,
                          collection_id=collection_id)
    created_member = member_crud.create(member)
    assert created_member.user_id == user_id
    assert created_member.collection_id == collection_id
    assert created_member.id is not None
    member_id = created_member.id

    # Assert
    assert len(member_crud.find_all()) == number_of_members + 1
    found_member = member_crud.find_by_id(member_id)
    assert found_member.user_id == created_user.id
    assert found_member.collection_id == created_collection.id
    assert found_member.id == created_member.id

    print(user_id, collection_id)

    # Act: find by user_id
    found_members = member_crud.find_by_user_id(str(user_id))
    assert len(found_members) == 1
    assert found_members[0].user_id == created_user.id
    assert found_members[0].collection_id == created_collection.id
    assert found_members[0].id == created_member.id

    # Act: find by collection_id
    found_members = member_crud.find_by_collection_id(collection_id)
    assert len(found_members) == 1
    assert found_members[0].user_id == created_user.id
    assert found_members[0].collection_id == created_collection.id
    assert found_members[0].id == created_member.id

    # Act: find by user_id, collection_id

    found_member = member_crud.find_by_user_id_and_collection_id(
        user_id, collection_id)
    assert found_member.user_id == created_user.id
    assert found_member.collection_id == created_collection.id
    assert found_member.id == created_member.id

    # Found by user_id, collection_id not in db
    found_not_existing_member = member_crud.find_by_user_id_and_collection_id(
        user_id, "0000")
    assert found_not_existing_member is None
    found_not_existing_member = member_crud.find_by_user_id_and_collection_id(
        "0000", collection_id)
    assert found_not_existing_member is None

    # Act: delete
    member_crud.delete(created_member)
    assert len(member_crud.find_all()) == number_of_members
    assert member_crud.find_by_id(created_member.id) is None
    user_crud.delete_by_id(user_id)
    collection_crud.delete_by_id(collection_id)
    assert user_crud.find_by_id(user_id) is None
    assert collection_crud.find_by_id(collection_id) is None
    assert len(member_crud.find_all()) == number_of_members
    assert member_crud.find_by_id(created_member.id) is None
