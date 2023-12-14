from fastapi_login import LoginManager
from datetime import timedelta

SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login', use_cookie=True,
                       default_expiry=timedelta(minutes=60))
