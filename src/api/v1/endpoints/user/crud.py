from src.models.models import UserInDBModel, UserModel
from src.config.env import user_collection
import bcrypt

user_collection.create_index("name", unique=True)


async def create_user(username: str, password: str) -> UserModel:
    """ Create a new user """
    password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    user = UserInDBModel(name=username, password=password)
    user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    user = await find_by_id(user.inserted_id)
    user = UserModel(**user.model_dump(by_alias=True))
    return user


async def find_by_id(id: str) -> UserModel:
    """
    Find a user by its unique id.
    """
    user = await user_collection.find_one({"_id": id})
    if user is None:
        return None
    return UserModel(**user)


async def find_by_username(username: str) -> UserInDBModel:
    """
    Find a user by its unique username.
    """
    user = await user_collection.find_one({"name": username})
    if user is None:
        return None
    return UserInDBModel(**user)
