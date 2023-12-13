from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()
templates = Jinja2Templates(directory="src/presentation/templates")

# Team id as a path parameter
@router.get("/{team_id}", response_class=HTMLResponse, name="devices")
async def get_chat(request: Request, team_id: str):
    # devices = device_crud.get_all_iotdevices(db)
    return templates.TemplateResponse("chat.html", {"request": request, "team_id": team_id})
