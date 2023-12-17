import src.api.v1.endpoints.collection.crud as collection_crud
from src.models.models import CreateCollectionModel


def test_collection_create_read_update_delete():
    collection_name = 'test_collection'
    collection = CreateCollectionModel(name=collection_name)
    number_of_collections = len(collection_crud.find_all())
    created_collection = collection_crud.create(collection)
    assert created_collection.name == collection_name
    assert created_collection.id is not None
    assert len(collection_crud.find_all()) == number_of_collections + 1
    found_collection = collection_crud.find_by_id(str(created_collection.id))
    assert found_collection.name == collection_name
    assert found_collection.id == created_collection.id
    updated_collection_name = 'updated_collection'
    update_collection = CreateCollectionModel(name=updated_collection_name)
    updated_collection = collection_crud.update(
        found_collection, update_collection)
    print(updated_collection)

    assert updated_collection.name == updated_collection_name
    assert updated_collection.id == created_collection.id
    assert len(collection_crud.find_all()) == number_of_collections + 1
    collection_crud.delete_by_id(updated_collection.id)
    assert len(collection_crud.find_all()) == number_of_collections
    assert collection_crud.find_by_id(created_collection.id) is None
