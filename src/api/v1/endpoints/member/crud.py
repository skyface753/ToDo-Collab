from typing import List
from src.models.models import MembersModel
from src.config.env import member_collection
from bson.objectid import ObjectId

member_collection.create_index(
    [("user_id", 1), ("collection_id", 1)], unique=True)


def create(member: MembersModel) -> MembersModel:
    """ Create a new Member """
    member = member_collection.insert_one(
        member.model_dump(by_alias=True, exclude=["id"])
    )
    member = find_by_id(member.inserted_id)
    return member


def find_by_id(id: str) -> MembersModel or None:
    """ Find a Member by its unique id. """
    member = member_collection.find_one({"_id": ObjectId(id)})
    if member is None:
        return None
    return MembersModel(**member)


def find_by_user_id(user_id: str) -> List[MembersModel]:
    """ Find all Member Relations by the user_id. """
    members = []
    for member in member_collection.find({"user_id": user_id}):
        members.append(MembersModel(**member))
    return members


def find_by_collection_id(collection_id: str) -> List[MembersModel]:
    """ Find all Member Relations by the collection_id. """
    members = []
    for member in member_collection.find({"collection_id": collection_id}):
        members.append(MembersModel(**member))
    return members


def find_by_user_id_and_collection_id(user_id: str, collection_id: str) \
        -> MembersModel or None:
    """ Find a Member by its unique user_id and collection_id. """
    member = member_collection.find_one(
        {"user_id": user_id, "collection_id": collection_id})
    if member is None:
        return None
    return MembersModel(**member)


def find_all() -> List[MembersModel]:
    """ Find all Members. """
    members = []
    for member in member_collection.find():
        members.append(MembersModel(**member))
    return members


def delete(member: MembersModel) -> None:
    """ Delete a Member. """
    member_collection.delete_one({"_id": ObjectId(member.id)})
