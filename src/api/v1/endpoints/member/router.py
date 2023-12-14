from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from src.models.models import MembersModel
import src.api.v1.endpoints.member.crud as member_crud

router = APIRouter()


@router.post("/create")
async def add_user_to_collection(request: Request, member: MembersModel):
    exists = await member_crud.find_by_user_id_and_collection_id(member.user_id, member.collection_id)
    if exists:
        url = request.url_for("collection", collection_id=member.collection_id)
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    return await member_crud.create(member.user_id, member.collection_id)
