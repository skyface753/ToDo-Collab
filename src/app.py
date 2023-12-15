from bson import json_util
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.presentation.endpoints.todo.router import router as todo_router
from src.api.v1.endpoints.todo.router import router as todo_router_api
from src.presentation.endpoints.collection.router import router as collection_router
from src.api.v1.endpoints.member.router import router as member_router_api
from src.api.v1.endpoints.collection.router import router as collection_router_api
from uvicorn.config import LOGGING_CONFIG
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from fastapi_login.exceptions import InvalidCredentialsException
import uvicorn
from src.handler.auth import manager
from src.api.v1.endpoints.user.crud import find_by_username as find_user_by_username, create_user as create_user

IS_DEV = True
app = FastAPI()


app.mount("/static", StaticFiles(directory="src/presentation/static"), name="static")


@manager.user_loader()
async def query_user(username: str):
    return await find_user_by_username(username)


@app.post('/login')
async def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = await query_user(username)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': username}
    )
    # response = RedirectResponse(
    #     url="/collection", status_code=status.HTTP_303_SEE_OTHER)
    manager.set_cookie(response, access_token)
    return {"access_token": access_token, "token_type": "bearer"}
    # return RedirectResponse(url="/todo/1", status_code=status.HTTP_303_SEE_OTHER)

templates = Jinja2Templates(directory="src/presentation/templates")


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post('/register')
async def register(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    # Check if user exists
    user = await query_user(username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    new_user = await create_user(username, password)
    return {'message': 'user created'}


@app.get('/protected')
def protected_route(user=Depends(manager)):
    return {'user': json_util.dumps(user)}


@app.get("/")
async def get():
    """ Redirect to the todo page """
    return RedirectResponse(url="/collection", status_code=status.HTTP_303_SEE_OTHER)

# Chat
app.include_router(todo_router, prefix="/todo", tags=["todo"])
app.include_router(todo_router_api, prefix="/api/v1/todo",
                   tags=["todo/api/v1"])
app.include_router(collection_router, prefix="/collection",
                   tags=["collection"])
app.include_router(member_router_api, prefix="/api/v1/member",
                   tags=["member/api/v1"])
app.include_router(collection_router_api, prefix="/api/v1/collection",
                   tags=["collection/api/v1"])


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
