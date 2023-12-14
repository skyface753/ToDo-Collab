from fastapi import APIRouter, Query, Depends
from src.models.models import TeamModel
from src.api.v1.endpoints.team.crud import team_collection
from src.handler.auth import manager as auth_manager
router = APIRouter()


@router.get("/")
async def get_my_teams(user=Depends(auth_manager)):
    user_id = user.id
    teams = await team_collection.find({"members": user_id}).to_list(length=100)
    return teams
