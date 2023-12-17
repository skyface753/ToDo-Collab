from pydantic import ConfigDict, BaseModel, Field, field_serializer
import uuid


class CreateTodoModel(BaseModel):
    """
    Create a new todo.
    """

    title: str = Field(..., min_length=1)
    description: str = Field(...)
    # Relation to the user
    user_name: str = Field(...)
    # Relation to the collection
    collection_id: uuid.UUID = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'title': 'Do the dishes',
                'description': 'Its your turn to do the dishes.',
                'user_id': 'User ID',
                'collection_id': 'Collection ID',  # NOSONAR
            },
        },
    )


class TodoModel(CreateTodoModel):
    id: uuid.UUID = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer('id')
    def serialize_id(self, id: uuid.UUID) -> str:
        return str(id)


class UserModel(BaseModel):
    """
    Create a new user.
    """

    name: str = Field(...)
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'name': 'User Name',
                'password': 'Your super secret password',
            },
        },
    )

    @field_serializer('password')
    def serialize_password(self, password: str) -> str:
        return '********'


class CreateCollectionModel(BaseModel):
    """
    Create a new collection.
    """

    name: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'name': 'Collection Name',
            },
        },

    )


class CollectionModel(CreateCollectionModel):
    """
    Container for a collection record.
    """

    id: uuid.UUID = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer('id')
    def serialize_id(self, id: uuid.UUID) -> str:
        return str(id)


class MembersModel(BaseModel):
    """
    Create a new member.
    """

    user_name: str = Field(...)
    collection_id: uuid.UUID = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            'example': {
                'user_id': 'User ID',
                'collection_id': 'Collection ID',  # NOSONAR
            },
        },
    )

    @field_serializer('collection_id')
    def serialize_collection_id(self, collection_id: uuid.UUID) -> str:
        return str(collection_id)
