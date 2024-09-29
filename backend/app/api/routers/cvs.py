import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.security.verify import roles_required

from app.core.postgres.models.user import Roles

from app.api.security.verify import get_current_user
from app.core.postgres.models.user import User

from app.core.mongodb.client import MongoDB, get_client

from app.core.mongodb.models.cv import CV

router = APIRouter()

logger = logging.getLogger('cvs')


@router.get(
    "/{cv_id}",
    dependencies=[Depends(roles_required(Roles.USER.value))]
)
async def get_cv(
    cv_id: str,
    mongodb_client: MongoDB = Depends(get_client),
    user: User = Depends(get_current_user)
):
    cv_collection = mongodb_client.collection('cvs')
    data = await cv_collection.fetch_one({'id': cv_id})
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'CV {cv_id} not found',
            headers={"WWW-Authenticate": "Bearer"}
        )

    return CV(**data)
