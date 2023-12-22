import src.api.v1.endpoints.member.crud as member_crud
import src.api.v1.endpoints.collection.crud as collection_crud
from src.models.models import CollectionModel, MembersModel, \
    UserModel, CreateCollectionModel
from typing import List


def find_collections_for_user(user_name: str) -> List[CollectionModel]:
    members = member_crud.find_by_user_name(user_name)
    collections = []
    for member in members:
        collection = collection_crud.find_by_id(member.collection_id)
        if collection is not None:
            collections.append(collection)
    return collections


def create_collection_for_user(collection: CreateCollectionModel,
                               user: UserModel) -> CollectionModel:
    collection = collection_crud.create(collection)
    member = MembersModel(user_name=user.name, collection_id=collection.id)
    member_crud.create(member)
    return collection
