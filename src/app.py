from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.endpoints.todo.router import router as todo_router
from src.api.v1.endpoints.todo.router import router as todo_router_api
from uvicorn.config import LOGGING_CONFIG
from src.config.env import user_collection
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from fastapi_login.exceptions import InvalidCredentialsException
import uvicorn
from src.handler.auth import manager

IS_DEV = True
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/presentation/static"), name="static")





@manager.user_loader()
async def query_user(email: str):
    return await user_collection.find_one({"email": email})

async def create_user(email: str, password: str):
    # Check if user exists
    user = await query_user(email)
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    if user:
        raise ValueError("User already exists")
    await user_collection.insert_one({"password": hashed, "email": email})

@app.post('/login')
async def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = await query_user(email)
    if not user:
        # you can return any response or error of your choice
        print("user not found")
        raise InvalidCredentialsException
    elif not bcrypt.checkpw(bytes(password, 'utf-8'), user['password']):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': email}
    )
    manager.set_cookie(response, access_token)
    return {'message': 'Logged in successfully'}
    # return RedirectResponse(url="/todo/1", status_code=status.HTTP_303_SEE_OTHER)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="src/presentation/templates")

@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.put('/register')
async def register(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    await create_user(email, password)
    return {'message': 'user created'}

from bson import json_util
@app.get('/protected')
def protected_route(user=Depends(manager)):
    print(user)
    return {'user': json_util.dumps(user)}


@app.get("/")
async def get():
    """ Redirect to the todo page """
    return RedirectResponse(url="/todo")

# Chat
app.include_router(todo_router, prefix="/todo", tags=["todo"])
app.include_router(todo_router_api, prefix="/api/v1/todo", tags=["todo/api/v1"])







def run():
    """ Run the application """
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = (
        "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    )
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
        '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - '
        '"%(request_line)s" %(status_code)s'
    )
    host = "127.0.0.1" if IS_DEV else "0.0.0.0"
    uvicorn.run(
        "src.app:app",
        host=host,
        port=8000,
        reload=bool(IS_DEV),
        log_config=LOGGING_CONFIG,
    )