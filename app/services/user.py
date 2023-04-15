
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, repository):
        self._repository = repository

    def add(self, user):
        
        item = User(
            **user.dict()
        )
        pwd = user.dict().get("password")
        if pwd:
            item.set_password(pwd)
        self._repository.create(item)
        return item

    def authenticate(self, name, password):
        return self._repository.authenticate(name, password)

    def update_pwd(self,user_id=None,password=None):
        return self._repository.update_pwd(user_id=user_id,password=password)
        
def get_default_user_service():
    return UserService(repository=UserRepository())
