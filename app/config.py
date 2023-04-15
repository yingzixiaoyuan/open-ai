# -*- encoding: utf-8 -*-

# @File    : config.py
# @Time    : 2021/12/24 14:54:32


import os

from pydantic import BaseSettings

APP_ENV = os.environ.get('APP_ENV',"dev")
PORTAL_USE_FAKE_INFO = os.environ.get("PORTAL_USE_FAKE_INFO", False)

if APP_ENV in ["prod"]:
    PORTAL_USE_FAKE_INFO = False

SECRET_KEY = "6e0ba8f73de7ffca6784703e9605217537efd1c1e38a89503b5b63c8848c85c0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

PORTAL_SKIP_URLS = [
    "/api/healthcheck",
    "/api/token"
]

class DevelopmentConfig(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

class ProductionConfig(BaseSettings):
    pass

class ProductionConfig(BaseSettings):
    pass


config = {
    "dev": DevelopmentConfig,
    "testing": ProductionConfig,
    "prod": ProductionConfig
}

settings = config[APP_ENV]
