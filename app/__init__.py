# -*- encoding: utf-8 -*-

# @File    : __init__.py
# @Time    : 2021/12/24 16:27:20
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app import config
from app.common.web import portal, request_scope
from app.common.web.api import error_response
from app.common.web.exception import WebError
from app.databases import Base, engine
from app.exceptions import InvalidBAError
from app.router import router

Base.metadata.create_all(bind=engine)

def get_app() -> FastAPI:
    if config.APP_ENV == "dev":
        app = FastAPI()
    else:
        app = FastAPI(redoc_url=None,docs_url=None)

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    # 开启cors（跨源资源共享）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 500字节以上才开启gzip
    app.add_middleware(
        GZipMiddleware,
        minimum_size=500
    )

    @app.middleware("http")
    async def request_ctx(request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        request_scope.set_request_id(request_id)
        response = await call_next(request)
        return response

    # 处理自定义exception
    @app.exception_handler(WebError)
    async def unicorn_exception_handler(request: Request, exc: WebError):
        return error_response(exc)

    @app.middleware("http")
    async def protal_auth(request: Request, call_next):
        try:
            portal.portal_auth(
                request=request,skip_urls=config.PORTAL_SKIP_URLS, use_fake_info=config.PORTAL_USE_FAKE_INFO
            )()
        except InvalidBAError as f:
            from app.common.web.api import error_response
            return error_response(f)
        response = await call_next(request)
        return response

    app.include_router(router, prefix="/api")

    return app
