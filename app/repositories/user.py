from app.exceptions import ResourceNotFound
from app.models.user import User
from app.repositories.base import RepositoryBase
from sqlalchemy.sql.expression import false


class UserRepository(RepositoryBase):
    DOMAIN_CLASS = User

    def __init__(self):
        super(UserRepository, self).__init__()

    def authenticate(self, name, password):
        auth_user = self.get_data_by_name(name=name)
        if auth_user:
            return self.DOMAIN_CLASS.check_password(auth_user, password)
        else:
            return False

    def update_pwd(self,user_id,password=None):
        item = self.db.query(self.DOMAIN_CLASS).filter(self.DOMAIN_CLASS.id == user_id).one()
        item.password = password
        self.update(item)

