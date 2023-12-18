from src.models.models import CollectionModel, CreateCollectionModel
from src.config.scylla import session
from typing import List
import uuid


def create_table():
    session.execute(
        'CREATE TABLE IF NOT EXISTS collections (id uuid PRIMARY KEY, name text)')


create_table()


def create(collection: CreateCollectionModel) -> CollectionModel:
    """ Create a new Collection """
    new_id = uuid.uuid4()
    session.execute(
        'INSERT INTO collections (id, name) VALUES (%s, %s)', (new_id, collection.name))
    collection = find_by_id(str(new_id))
    return collection


def find_by_id(id: str) -> CollectionModel or None:
    """
    Find a collection by its unique id.
    """
    results = session.execute(
        'SELECT * FROM collections WHERE id = %s', (uuid.UUID(str(id)),))
    for result in results:
        return CollectionModel(id=result.id, name=result.name)
    return None


def find_all() -> List[CollectionModel]:
    """
    Find all collections.
    """
    results = session.execute('SELECT * FROM collections')
    collections = []
    for result in results:
        collections.append(CollectionModel(id=result.id, name=result.name))
    return collections


def update(collection: CollectionModel, updated_collection: CreateCollectionModel) \
        -> CollectionModel:
    """
    Update a collection.
    """
    session.execute(
        'UPDATE collections SET name = %s WHERE id = %s', (updated_collection.name, collection.id))
    return find_by_id(collection.id)


def delete_by_id(id: str) -> None:
    """
    Delete a collection.
    """
    session.execute('DELETE FROM collections WHERE id = %s',
                    (uuid.UUID(str(id)),))
