from src.models.models import CollectionModel
from src.config.env import collection_collection
# import src.api.v1.endpoints.member.crud as member_crud
from bson.objectid import ObjectId

# collection_collection.create_index("name", unique=True)


async def create(name: str) -> CollectionModel:
    """ Create a new Collection """
    collection = CollectionModel(name=name)
    collection = await collection_collection.insert_one(
        collection.model_dump(by_alias=True, exclude=["id"])
    )
    collection = await find_by_id(collection.inserted_id)
    return collection


async def find_by_name(name: str) -> CollectionModel:
    """
    Find a collection by its unique name.
    """
    collection = await collection_collection.find_one({"name": name})
    if collection is None:
        return None
    return CollectionModel(**collection)


async def find_by_id(id: str) -> CollectionModel:
    """
    Find a collection by its unique id.
    """
    object_id = ObjectId(id)
    collection = await collection_collection.find_one({"_id": object_id})
    if collection is None:
        return None
    return CollectionModel(**collection)
