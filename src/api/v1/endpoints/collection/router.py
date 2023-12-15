from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from src.handler.auth import manager as auth_manager
from src.logic.collection import find_collections_for_user

router = APIRouter()


@router.post("/")
async def get_collections(user=Depends(auth_manager)):
    collections = await find_collections_for_user(user.id)
    return collections
