from fastapi import APIRouter, Depends, status, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.handler.auth import auth_manager
from src.handler.auth import query_user
import bcrypt
from fastapi_login.exceptions import InvalidCredentialsException
from bson import json_util
from src.models.models import UserModel
import src.api.v1.endpoints.user.crud as user_crud
import src.logic.user as user_logic
import datetime

router = APIRouter()

templates = Jinja2Templates(directory='src/presentation/templates')

timedelta_default = auth_manager.default_expiry
timedelta_remember = datetime.timedelta(days=30)


@router.get('/login', response_class=HTMLResponse, name='login')
def login_page(request: Request, error: str = None):
    return templates.TemplateResponse('login.html.jinja2', {'request': request, 'error': error})


@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: Request, login_user: UserModel, remember: bool = False):
    user = query_user(login_user.name)
    if not user or not bcrypt.checkpw(bytes(login_user.password, 'utf-8'),
                                      bytes(user.password, 'utf-8')):
        return InvalidCredentialsException

    access_token = auth_manager.create_access_token(
        data={'sub': user.name},
        expires=timedelta_remember if remember else timedelta_default,
    )
    user.password = None
    data = {'message': 'Logged in as ' + user.name, 'access_token': access_token,
            'user': user.model_dump()}
    rsp = Response(content=json_util.dumps(data),
                   media_type='application/json')  # NOSONAR
    auth_manager.set_cookie(rsp, access_token)
    return rsp


@router.get('/register', response_class=HTMLResponse, name='register')
def register_page(request: Request, error: str = None):
    return templates.TemplateResponse('register.html.jinja2', {'request': request, 'error': error})


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(request: Request, register_user: UserModel, remember: bool = False):
    # Check if user exists
    user = query_user(register_user.name)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User already exists')
    user_crud.create(register_user)
    rsp = Response(content=json_util.dumps({'message': 'User created successfully'}),
                   media_type='application/json',  # NOSONAR
                   status_code=status.HTTP_201_CREATED)
    auth_manager.set_cookie(rsp, auth_manager.create_access_token(
        data={'sub': register_user.name},
        expires=timedelta_remember if remember else timedelta_default,
    ))
    return rsp


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(user=Depends(auth_manager)):
    # Check if user exists
    user = query_user(user.name)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User does not exist')
    user_logic.delete_user_cascade(user)

    return {'message': 'User deleted'}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, request: Request):
    rsp = RedirectResponse(request.url_for(
        'login'), status_code=status.HTTP_303_SEE_OTHER)
    rsp.delete_cookie('access-token')
    return rsp
