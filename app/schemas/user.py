# -*- encoding: utf-8 -*-

# @File    : user.py
# @Time    : 2021/11/06 22:13:07


from typing import List

from pydantic import BaseModel, root_validator, validator
from pydantic.errors import PydanticValueError

from .item import Item


class UserBase(BaseModel):
    name: str

    # @validator("name")
    # def name_validator(cls, name):
    #     if name.isdigit():
    #         raise ValueError('incorrect name')
    #     return name
    # @root_validator
    # def root_validator_test(cls, fields):
    #   	if not any(fields.values("at least one parameter")):
    #       	raise PydanticValueError()
    #     return fields


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
