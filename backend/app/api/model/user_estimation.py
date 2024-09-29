from pydantic import BaseModel

from app.model.estimation import Estimation
from app.model.user import User


class PageRestrictions(BaseModel):
    gym: bool
    rest: bool
    work: bool
    start: bool


class UserEstimationsDataModel(BaseModel):
    user: User
    estimation: Estimation
