import json
import logging
import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from starlette.responses import JSONResponse

from app.core.postgres.models.user import User, Roles

from app.api.security.verify import roles_required

from app.api.security.verify import get_current_user
from app.core.qdrant import client as qdrant_client

import config
from pydantic import ValidationError

from app.core.mongodb.models.cv import CV

from app.core.mongodb.client import MongoDB, get_client

from app.core.qdrant.representations.cv import cv_represent

logger = logging.getLogger("app.api.routers.parser")

router = APIRouter()

UPLOAD_DIRECTORY = config.env_param('UPLOAD_DIR')


languages: dict[str, str] = {
    "Romanian": "RO",
    "Russian": "RU",
    "English": "EN-US",
}


async def __save_document(position: str, language: str, document: UploadFile = File(...)) -> str:
    position_directory = os.path.join(UPLOAD_DIRECTORY, position, language)
    if not os.path.exists(position_directory):
        os.makedirs(position_directory)

    file_location = os.path.join(position_directory, document.filename)

    with open(file_location, "wb") as buffer:
        buffer.write(await document.read())

    # You can process the description and other form data here
    return config.env_param('APP_BASE') + file_location


@router.post(
    '/upload',
    dependencies=[Depends(roles_required(Roles.PARSER.value))]
)
async def update_or_add_configuration(
    document: UploadFile = File(...),
    data: str = Form(...),
    mongodb_client: MongoDB = Depends(get_client),
    user: User = Depends(get_current_user)
):
    logger.info(f'Received CV {document.filename}')
    cv_collection = mongodb_client.collection('cvs')

    try:
        data = json.loads(data)

        cv = CV(**data)
        cv.id = str(uuid.uuid4())
        cv.lang = data['cv_language']
        cv.document_url = await __save_document(cv.job_position, cv.lang, document)
        await qdrant_client.insert(
            cv_represent(cv),
            cv.model_dump(by_alias=True)
        )
        await cv_collection.insert(cv.model_dump(by_alias=True))
    except ValidationError as e:
        logger.info(e.json())
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.json(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.info(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'saved': True}
    )