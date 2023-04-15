# -*- encoding: utf-8 -*-

# @File    : router.py
# @Time    : 2021/11/06 23:57:26



# from items import router as router_item
from fastapi import APIRouter

from app.apis.healthcheck import router as router_healthcheck
from app.apis.v1.token.login import router as router_token
from app.apis.v1.user.user import router as router_users

router = APIRouter()

router.include_router(router_healthcheck,tags=["healthcheck"])
router.include_router(router_users, tags=["users"])
router.include_router(router_token, tags=["token"])


