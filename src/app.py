from src.models.models import UserModel
from bson import json_util
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, status, HTTPException, Response
from fastapi.responses import RedirectResponse, HTMLResponse
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
import src.api.v1.endpoints.user.crud as user_crud
import src.logic.user as user_logic

IS_DEV = True
app = FastAPI()


app.mount("/static", StaticFiles(directory="src/presentation/static"), name="static")


@manager.user_loader()
def query_user(username: str):
    return user_crud.find_by_username(username)


@app.post('/login', status_code=status.HTTP_200_OK)
def login_user(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = query_user(username)
    if not user or not bcrypt.checkpw(bytes(password, 'utf-8'),
                                      bytes(user.password, 'utf-8')):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': username}
    )
    user.password = None
    url = str(request.url_for('collections'))
    print(url)
    headers = {'Location': url}
    username = user.name
    data = {'message': 'Logged in as ' + username, 'access_token': access_token,
            'user': user.model_dump(exclude=["password"])}
    rsp = Response(content=json_util.dumps(data), media_type="application/json",
                   status_code=status.HTTP_303_SEE_OTHER, headers=headers)
    manager.set_cookie(rsp, access_token)
    return rsp


templates = Jinja2Templates(directory="src/presentation/templates")


@app.get('/login', response_class=HTMLResponse, name="login")
async def login(request: Request):
    return templates.TemplateResponse("login.html.jinja2", {"request": request})


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    # Check if user exists
    user = query_user(username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    user = UserModel(name=username, password=password)
    user_crud.create(user)
    return {'message': 'User created successfully'}


@app.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    # Check if user exists
    user = query_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User does not exist")
    if not bcrypt.checkpw(bytes(password, 'utf-8'),
                          bytes(user.password, 'utf-8')):
        raise InvalidCredentialsException
    user_logic.delete_user_cascade(user)

    return {"message": "User deleted"}


@app.get('/protected')
def protected_route(user=Depends(manager)):
    return {'user': json_util.dumps(user)}


@app.get("/")
def get(request: Request, user=Depends(manager.optional)):
    """ Redirect to the todo page """
    if user:
        return RedirectResponse(url=request.url_for('collections'),
                                status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(url=request.url_for('login'),
                                status_code=status.HTTP_303_SEE_OTHER)


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
