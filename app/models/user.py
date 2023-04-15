# -*- encoding: utf-8 -*-

# @File    : user.py
# @Time    : 2021/11/06 23:59:16



from app.databases import Base
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)

