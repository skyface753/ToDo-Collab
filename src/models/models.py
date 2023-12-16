from pydantic import ConfigDict, BaseModel, Field
from typing import Optional
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId


PyObjectId = Annotated[str, BeforeValidator(str)]


class TodoModel(BaseModel):
    """
    Container for a todo record.
    """

    # The primary key for the TodoModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=1)
    description: str = Field(...)
    # Relation to the user
    user_id: str = Field(...)
    # Relation to the collection
    collection_id: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Do the dishes",
                "description": "It's your turn to do the dishes.",
                "user_id": "User ID",
                "collection_id": "Collection ID",  # NOSONAR
            }
        },
        json_encoders={ObjectId: str},
    )


class UserModel(BaseModel):
    """
    Container for a user record.
    """

    # The primary key for the TodoModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "User Name",
                "password": "Your super secret password",
            }
        },
    )


class CreateCollectionModel(BaseModel):
    """
    Create a new collection.
    """

    name: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Collection Name",
            }
        },
    )


class CollectionModel(BaseModel):
    """
    Container for a Collection record.
    Collections are used to group todos.
    """

    id: PyObjectId = Field(alias="_id", default=ObjectId())
    name: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "Collection ID",  # NOSONAR
                "name": "Collection Name",
            }
        },
        json_encoders={ObjectId: str},
    )


class MembersModel(BaseModel):
    """
    Relation between a user and collection.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str = Field(..., min_length=1)
    collection_id: str = Field(..., min_length=1)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "User ID",
                "collection_id": "Collection ID",  # NOSONAR
            }
        },
    )
