from pydantic import ConfigDict, BaseModel, Field, EmailStr
from typing import Optional, List
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
    title: str = Field(...)
    description: str = Field(...)
    # Relation to the user
    user_id: str = Field(...)
    # user_name: Optional[str] = None
    # Relation to the collection
    collection_id: str = Field(...)
    # collection_name: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Do the dishes",
                "description": "It's your turn to do the dishes.",
                "user_id": "User ID",
                "collection_id": "Collection ID",
            }
        },
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


class CollectionModel(BaseModel):
    """
    Container for a Collection record.
    Collections are used to group todos.
    """

    # The primary key for the TodoModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
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


class MembersModel(BaseModel):
    """
    Relation between a user and collection.
    """

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str = Field(...)
    collection_id: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "User ID",
                "collection_id": "Collection ID",
            }
        },
    )


class TodoCollection(BaseModel):
    """
    A container holding a list of `TodoModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    todos: List[TodoModel]


# class UpdateStudentModel(BaseModel):
#     """
#     A set of optional updates to be made to a document in the database.
#     """

#     name: Optional[str] = None
#     email: Optional[EmailStr] = None
#     course: Optional[str] = None
#     gpa: Optional[float] = None
#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str},
#         json_schema_extra={
#             "example": {
#                 "name": "Jane Doe",
#                 "email": "jdoe@example.com",
#                 "course": "Experiments, Science, and Fashion in Nanophotonics",
#                 "gpa": 3.0,
#             }
#         },
#     )


# class StudentCollection(BaseModel):
#     """
#     A container holding a list of `StudentModel` instances.

#     This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
#     """

#     students: List[StudentModel]
