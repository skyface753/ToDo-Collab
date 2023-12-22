from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.api.v1.endpoints.todo.router import router as todo_router_api
from src.presentation.endpoints.collection.router import router as collection_router
from src.api.v1.endpoints.member.router import router as member_router_api
from src.api.v1.endpoints.collection.router import router as collection_router_api
from src.presentation.endpoints.auth.router import router as auth_router
from src.api.v1.endpoints.user.router import router as user_router_api
from uvicorn.config import LOGGING_CONFIG
from fastapi import Depends
import uvicorn
from src.handler.auth import auth_manager, NotAuthenticatedException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging


IS_DEV = True
app = FastAPI()

app.mount('/static', StaticFiles(directory='src/presentation/static'), name='static')


@app.get('/')
def get(request: Request, user=Depends(auth_manager.optional)):
    """ Redirect to the todo page """
    if user:
        return RedirectResponse(url=request.url_for('collections'),
                                status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse(url=request.url_for('login'),
                            status_code=status.HTTP_303_SEE_OTHER)


# Jinja Presentation
app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(collection_router, prefix='/collection',
                   tags=['collection'])
# API
app.include_router(todo_router_api, prefix='/api/v1/todo',
                   tags=['todo/api/v1'])
app.include_router(member_router_api, prefix='/api/v1/member',
                   tags=['member/api/v1'])
app.include_router(collection_router_api, prefix='/api/v1/collection',
                   tags=['collection/api/v1'])
app.include_router(user_router_api, prefix='/api/v1/user',
                   tags=['user/api/v1'])


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    # Check if it was an API request
    if request.url.path.startswith('/api'):
        return JSONResponse(content={'message': 'Not authenticated'}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return RedirectResponse(url=request.url_for('login'))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f'{request}: {exc_str}')
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def run():
    """ Run the application """
    LOGGING_CONFIG['formatters']['default']['fmt'] = (
        '%(asctime)s [%(name)s] %(levelprefix)s %(message)s'
    )
    LOGGING_CONFIG['formatters']['access']['fmt'] = (
        '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - '
        '"%(request_line)s" %(status_code)s'
    )
    host = '127.0.0.1' if IS_DEV else '0.0.0.0'
    uvicorn.run(
        'src.app:app',
        host=host,
        port=8000,
        reload=bool(IS_DEV),
        log_config=LOGGING_CONFIG,
    )
