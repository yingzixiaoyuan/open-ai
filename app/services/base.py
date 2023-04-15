class BaseService():

    def list(self, skip=None, limit=None):
        return self._repository.list(skip=skip, limit=limit)

    def get_data_by_name(self, name=None):
        return self._repository.get_data_by_name(name=name)

    def get_data_by_like_name(self, name=None):
        return self._repository.get_data_by_like_name(name=name)

    def get_data_by_id(self, id=None):
        return self._repository.get_data_by_id(id=id)

    def delete(self, id):
        item = self._repository.get_data_by_id(id=id)
        return self._repository.delete(item)

    def update(self, item=None):
        return self._repository.update(self._repository.get_data_by_id(id=item.id), kwargs=item.dict())
