from fastapi import APIRouter, Depends, status, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.handler.auth import auth_manager
from src.handler.auth import query_user
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from fastapi_login.exceptions import InvalidCredentialsException
from bson import json_util
from src.models.models import UserModel
import src.api.v1.endpoints.user.crud as user_crud
import src.logic.user as user_logic


router = APIRouter()

templates = Jinja2Templates(directory='src/presentation/templates')


@router.get('/login', response_class=HTMLResponse, name='login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html.jinja2', {'request': request})


@router.post('/login', status_code=status.HTTP_200_OK)
def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = query_user(username)
    if not user or not bcrypt.checkpw(bytes(password, 'utf-8'),
                                      bytes(user.password, 'utf-8')):
        raise InvalidCredentialsException

    access_token = auth_manager.create_access_token(
        data={'sub': username},
    )
    user.password = None
    url = str(request.url_for('collections'))
    print(url)
    headers = {'Location': url}
    username = user.name
    data = {'message': 'Logged in as ' + username, 'access_token': access_token,
            'user': user.model_dump()}
    rsp = Response(content=json_util.dumps(data), media_type='application/json',
                   status_code=status.HTTP_303_SEE_OTHER, headers=headers)
    auth_manager.set_cookie(rsp, access_token)
    return rsp


@router.get('/register', response_class=HTMLResponse, name='register')
def register_page(request: Request):
    return templates.TemplateResponse('register.html.jinja2', {'request': request})


@router.post('/register', status_code=status.HTTP_201_CREATED)
def register(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    # Check if user exists
    user = query_user(username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User already exists')
    user = UserModel(name=username, password=password)
    user_crud.create(user)
    url = str(request.url_for('collections'))
    headers = {'Location': url}
    rsp = Response(content=json_util.dumps({'message': 'User created successfully'}),
                   media_type='application/json',
                   status_code=status.HTTP_303_SEE_OTHER, headers=headers)
    auth_manager.set_cookie(rsp, auth_manager.create_access_token(
        data={'sub': username},
    ))
    return rsp


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    # Check if user exists
    user = query_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User does not exist')
    if not bcrypt.checkpw(bytes(password, 'utf-8'),
                          bytes(user.password, 'utf-8')):
        raise InvalidCredentialsException
    user_logic.delete_user_cascade(user)

    return {'message': 'User deleted'}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, request: Request):
    response = RedirectResponse(request.url_for(
        'login'), status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie('access-token')
    return response
