SECRET = "super-secret-key"
from fastapi_login import LoginManager
manager = LoginManager(SECRET, '/login', use_cookie=True)