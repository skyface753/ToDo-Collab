from fastapi import APIRouter, Request, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.handler.auth import manager
import json

router = APIRouter()
templates = Jinja2Templates(directory="src/presentation/templates")

# Team id as a path parameter


# @router.get("/{collection_id}", response_class=HTMLResponse, name="devices")
# async def get_chat(request: Request, collection_id: str, user=Depends(manager.optional)):
#     token = await manager._get_token(request)
#     if user:
#         user = json.loads(json.dumps(user, default=lambda o: str(o)))
#         return templates.TemplateResponse("chat.html", {"request": request, "collection_id": collection_id, "user": user, "token": token})
#     else:
#         return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
# 202774af4b864f98f50f

# from bson import json_util
# @app.get('/protected')
# def protected_route(user=Depends(manager)):
#     print(user)
#     return {'user': json_util.dumps(user)}
