from src.models.models import CollectionModel
from src.config.env import collection_collection
from bson.objectid import ObjectId
from typing import List

collection_collection.create_index("name", unique=True)


def create(collection: CollectionModel) -> CollectionModel:
    """ Create a new Collection """
    collection = collection_collection.insert_one(
        collection.model_dump(by_alias=True, exclude=["id"])
    )
    collection = find_by_id(collection.inserted_id)
    return collection


def find_by_name(name: str) -> CollectionModel or None:
    """
    Find a collection by its unique name.
    """
    collection = collection_collection.find_one({"name": name})
    if collection is None:
        return None
    return CollectionModel(**collection)


def find_by_id(id: str) -> CollectionModel or None:
    """
    Find a collection by its unique id.
    """
    collection = collection_collection.find_one({"_id": ObjectId(id)})
    if collection is None:
        return None
    return CollectionModel(**collection)


def find_all() -> List[CollectionModel]:
    """
    Find all collections.
    """
    collections = []
    for collection in collection_collection.find():
        collections.append(CollectionModel(**collection))
    return collections


def update(collection: CollectionModel, updated_collection: CollectionModel) \
        -> CollectionModel:
    """
    Update a collection.
    """
    for field, value in updated_collection:
        if value is not None:
            setattr(collection, field, value)
    print("New collection: ", collection.model_dump(by_alias=True))
    result = collection_collection.update_one({"_id": ObjectId(collection.id)}, {
                                              "$set": {"name": collection.name}})
    print("Result: ", result)
    return find_by_id(collection.id)


def delete_by_id(id: str) -> None:
    """
    Delete a collection.
    """
    collection_collection.delete_one({"_id": ObjectId(id)})
