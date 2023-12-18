from src.models.models import UserModel
from src.config.scylla import session
import bcrypt
from typing import List


def create_table():
    session.execute(
        'CREATE TABLE IF NOT EXISTS users (name text PRIMARY KEY, password text)')


create_table()


def create(user: UserModel) -> UserModel:
    """ Create a new user """
    password = user.password
    hashed_password = bcrypt.hashpw(
        bytes(password, 'utf-8'), bcrypt.gensalt())
    user.password = str(hashed_password, 'utf-8')
    session.execute(
        'INSERT INTO users (name, password) VALUES (%s, %s)', (user.name, user.password))
    user = find_by_username(user.name)
    return user


def find_by_username(username: str) -> UserModel or None:
    """
    Find a user by its unique username.
    """
    results = session.execute(
        'SELECT * FROM users WHERE name = %s', (username,))
    for result in results:
        return UserModel(name=result.name, password=result.password)
    return None


def find_all() -> List[UserModel]:
    """
    Find all users.
    """
    users = []
    results = session.execute('SELECT * FROM users')
    for result in results:
        users.append(UserModel(name=result.name, password=result.password))
    return users


def delete_by_name(name: str) -> None:
    """
    Delete a user by its unique name.
    """
    session.execute('DELETE FROM users WHERE name = %s', (name,))
