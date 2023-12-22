from typing import List
from src.models.models import MembersModel
from src.config.scylla import session
import uuid


def create_table():
    session.execute(
        """
        CREATE TABLE IF NOT EXISTS members
        (user_name text, collection_id uuid, PRIMARY KEY (user_name, collection_id))
        """,
    )


create_table()


def create(member: MembersModel) -> MembersModel:
    """ Create a new Member """
    session.execute(
        'INSERT INTO members (user_name, collection_id) VALUES (%s, %s)',
        (member.user_name, member.collection_id))
    member = find_by_user_name_and_collection_id(
        member.user_name, member.collection_id)
    return member


def find_by_user_name(user_name: str) -> List[MembersModel]:
    """ Find all Member Relations by the user_name. """
    members = []
    results = session.execute(
        'SELECT * FROM members WHERE user_name = %s', (user_name,))
    for result in results:
        members.append(MembersModel(user_name=result.user_name,
                       collection_id=result.collection_id))
    return members


def find_by_collection_id(collection_id: str) -> List[MembersModel]:
    """ Find all Member Relations by the collection_id. """
    members = []
    results = session.execute(
        'SELECT * FROM members WHERE collection_id = %s', (collection_id,))
    for result in results:
        members.append(MembersModel(user_name=result.user_name,
                       collection_id=result.collection_id))
    return members


def find_by_user_name_and_collection_id(user_name: str, collection_id: str) \
        -> MembersModel or None:
    """ Find a Member by its unique user_name and collection_id. """
    collection_id = uuid.UUID(str(collection_id))
    results = session.execute(
        'SELECT * FROM members WHERE user_name = %s AND collection_id = %s',
        (user_name, collection_id))
    for result in results:
        print(result)
        return MembersModel(user_name=result.user_name, collection_id=result.collection_id)
    return None


def find_all() -> List[MembersModel]:
    """ Find all Members. """
    members = []
    results = session.execute('SELECT * FROM members')
    for result in results:
        members.append(MembersModel(user_name=result.user_name,
                       collection_id=result.collection_id))
    return members


def delete_by_user_name_and_collection_id(user_name: str, collection_id: str) -> List[MembersModel]:
    """ Delete a Member by its unique user_name and collection_id. """
    members = find_by_user_name_and_collection_id(user_name, collection_id)
    session.execute('DELETE FROM members WHERE user_name = %s AND collection_id = %s',
                    (user_name, collection_id))
    return members


def delete_by_user_name(user_name: str) -> List[MembersModel]:
    """ Delete all Member Relations by the user_name.
        Returns the deleted members. (for cleanup cascade)
    """
    members = find_by_user_name(user_name)
    session.execute('DELETE FROM members WHERE user_name = %s', (user_name,))
    return members
