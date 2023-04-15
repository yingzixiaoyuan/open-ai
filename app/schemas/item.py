# -*- encoding: utf-8 -*-

# @File    : item.py
# @Time    : 2021/11/06 22:13:02



from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
