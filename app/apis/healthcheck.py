# -*- encoding: utf-8 -*-

# @File    : healthcheck.py
# @Time    : 2021/12/24 13:40:08


from fastapi import APIRouter

router = APIRouter()

@router.get("/healthcheck")
async def healthcheck():
    return "ok"
