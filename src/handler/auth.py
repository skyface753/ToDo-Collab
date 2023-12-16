from fastapi_login import LoginManager
from datetime import timedelta
import src.api.v1.endpoints.user.crud as user_crud
from src.config.env import AUTH_SECRET


class NotAuthenticatedException(Exception):
    pass


auth_manager = LoginManager(AUTH_SECRET, '/login', use_cookie=True,
                            default_expiry=timedelta(minutes=60),
                            custom_exception=NotAuthenticatedException)


@auth_manager.user_loader()
def query_user(username: str):
    return user_crud.find_by_username(username)
