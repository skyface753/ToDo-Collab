from fastapi import APIRouter, status, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import src.logic.user as user_logic

router = APIRouter()

templates = Jinja2Templates(directory='src/presentation/templates')


@router.get('/login', response_class=HTMLResponse, name='login')
def login_page(request: Request):
    return templates.TemplateResponse('login.html.jinja2', {'request': request})


@router.get('/register', response_class=HTMLResponse, name='register')
def register_page(request: Request):
    return templates.TemplateResponse('register.html.jinja2', {'request': request})


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, request: Request):
    rsp = RedirectResponse(request.url_for(
        'login'), status_code=status.HTTP_303_SEE_OTHER)
    rsp = user_logic.logout(rsp)
    rsp.delete_cookie('access-token')
    return rsp
