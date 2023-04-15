# -*- encoding: utf-8 -*-

# @File    : user.py
# @Time    : 2021/11/06 23:58:26

from app.common.web.api import json_response
from app.exceptions import ResourceExist
from app.schemas import user as user_schema
from app.services.user import get_default_user_service
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.post("/users/")
@json_response
def add(user: user_schema.UserCreate):
    db_user = get_default_user_service(
    ).get_data_by_name(name=user.name)
    if db_user:
        raise ResourceExist(message="user already existed")
    get_default_user_service().add(user=user)
