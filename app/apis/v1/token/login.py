from app import config
from app.common.web.api import json_response
from app.common.web.portal import Portal
from app.exceptions import AuthorizedError
from app.schemas import token as token_schema
from app.services.user import get_default_user_service
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@json_response
@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(request: Request,data: OAuth2PasswordRequestForm = Depends()):
    name = data.username
    password = data.password
    if not get_default_user_service().authenticate(name,password):
        raise AuthorizedError
    else:
        access_token = Portal(request, config.SECRET_KEY).encode_auth_token(name)
        return {"access_token": access_token, "token_type": "bearer"}
