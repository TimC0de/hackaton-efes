import logging

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.core.postgres.models.user import User, Roles

from app.api.security.verify import roles_required, get_current_user
from pydantic import BaseModel

from app.api.security.hash import get_password_hash
from app.core.postgres.queries import role, user

logger = logging.getLogger("app.api.routers.user")

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    password: str
    roles: list[str]


@router.post(
    '/',
    dependencies=[Depends(roles_required(Roles.ADMIN.value))]
)
async def create_user(
    data: UserCreate,
    current_user: User = Depends(get_current_user)
):
    existing_user = await user.get_by_username(data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Hash the password
    hashed_password = get_password_hash(data.password)

    # Fetch roles from the database
    roles = await role.get_by_names(data.roles)
    if not roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid roles provided")

    # Create and add new user to the database
    new_user = User(username=data.username, hashed_password=hashed_password, roles=roles)
    await user.insert(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}