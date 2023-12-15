from src.models.models import UserModel
from src.config.env import user_collection
import bcrypt
from bson.objectid import ObjectId
from typing import List

user_collection.create_index("name", unique=True)


def create(user: UserModel) -> UserModel:
    """ Create a new user """
    password = user.password
    hashed_password = bcrypt.hashpw(
        bytes(password, 'utf-8'), bcrypt.gensalt())
    user.password = str(hashed_password, 'utf-8')
    user = user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"]))
    user = user_collection.find_one({"_id": user.inserted_id})
    return UserModel(**user)


def find_by_id(id: str) -> UserModel or None:
    """
    Find a user by its unique id.
    """
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user is None:
        return None
    return UserModel(**user)


def find_by_username(username: str) -> UserModel or None:
    """
    Find a user by its unique username.
    """
    user = user_collection.find_one({"name": username})
    if user is None:
        return None
    return UserModel(**user)


def find_all() -> List[UserModel]:
    """
    Find all users.
    """
    users = []
    for user in user_collection.find():
        users.append(UserModel(**user))
    return users


def delete_by_id(id: str) -> None:
    """
    Delete a user by its unique id.
    """
    user_collection.delete_one({"_id": ObjectId(id)})
