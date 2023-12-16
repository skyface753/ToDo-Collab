from fastapi_login import LoginManager
from datetime import timedelta
import src.api.v1.endpoints.user.crud as user_crud

SECRET = "super-secret-key"
auth_manager = LoginManager(SECRET, '/login', use_cookie=True,
                            default_expiry=timedelta(minutes=60))


@auth_manager.user_loader()
def query_user(username: str):
    return user_crud.find_by_username(username)
