from typing import List
from src.models.models import MembersModel
from src.config.env import member_collection
from bson.objectid import ObjectId

member_collection.create_index(
    [("user_id", 1), ("collection_id", 1)], unique=True)


async def create(user_id: str, collection_id: str) -> MembersModel:
    """ Create a new Member """
    member = MembersModel(user_id=user_id, collection_id=collection_id)
    member = await member_collection.insert_one(
        member.model_dump(by_alias=True, exclude=["id"])
    )
    member = await find_by_id(member.inserted_id)
    return member


async def find_by_id(id: str) -> MembersModel:
    """ Find a Member by its unique id. """
    object_id = ObjectId(id)
    member = await member_collection.find_one({"_id": object_id})
    if member is None:
        return None
    return MembersModel(**member)


async def find_by_user_id(user_id: str) -> List[MembersModel]:
    """ Find all Member by its unique user_id. """
    member = await member_collection.find({"user_id": user_id}).to_list(length=100)
    if member is None:
        return None
    return [MembersModel(**m) for m in member]


async def find_by_collection_id(collection_id: str) -> List[MembersModel]:
    """ Find all Member by its unique collection_id. """
    member = await member_collection.find({"collection_id": collection_id}).to_list(length=100)
    if member is None:
        return None
    return [MembersModel(**m) for m in member]


async def find_by_user_id_and_collection_id(user_id: str, collection_id: str) -> MembersModel:
    """ Find a Member by its unique user_id and collection_id. """
    member = await member_collection.find_one({"user_id": user_id, "collection_id": collection_id})
    if member is None:
        return None
    return MembersModel(**member)
