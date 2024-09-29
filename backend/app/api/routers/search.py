import logging

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security.verify import roles_required

from app.core.postgres.models.user import Roles

from app.api.security.verify import get_current_user
from app.core.postgres.models.user import User

from app.core.qdrant import client as qdrant_client

router = APIRouter()

logger = logging.getLogger('auth')


@router.get(
    "/",
    dependencies=[Depends(roles_required(Roles.PARSER.value))]
)
async def search_cvs(
    query: str,
    language: str,
    user: User = Depends(get_current_user)
):
    return await qdrant_client.search(language, query)