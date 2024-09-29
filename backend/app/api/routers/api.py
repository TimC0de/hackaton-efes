from app.api.routers import auth, parser, user, search, cvs
from fastapi import APIRouter
from fastapi.responses import JSONResponse

api_router = APIRouter()
api_router.prefix = "/api"
api_router.default_response_class = JSONResponse


api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(parser.router, prefix="/parser", tags=["Parser"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(cvs.router, prefix="/cvs", tags=["CVs"])