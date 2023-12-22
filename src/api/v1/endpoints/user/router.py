from fastapi import APIRouter, Depends, status, Response, Request, HTTPException
from src.models.models import UserModel
from src.handler.auth import auth_manager, query_user
import datetime
import src.logic.user as user_logic
import bcrypt
from bson import json_util
import src.api.v1.endpoints.user.crud as user_crud
router = APIRouter()


timedelta_default = auth_manager.default_expiry
timedelta_remember = datetime.timedelta(days=30)


@router.post('/login', status_code=status.HTTP_200_OK, name='login_api')
def login(request: Request, login_user: UserModel, remember: bool = False):
    user = query_user(login_user.name)
    if not user or not bcrypt.checkpw(bytes(login_user.password, 'utf-8'),
                                      bytes(user.password, 'utf-8')):
        # return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid username or password')

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


@router.post('/register', status_code=status.HTTP_201_CREATED, name='register_api')
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


@router.post('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response):
    rsp = user_logic.logout(response)
    return rsp
