from app.databases import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RepositoryBase:
    DOMAIN_CLASS = None

    def __init__(self) -> None:
        self.db = next(get_db())

    def save(self):
        self.db.add(self)
        return self

    def create(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_data_by_like_name(self, name: str = None):
        search = "%{}%".format(name)
        return self.db.query(self.DOMAIN_CLASS).filter(self.DOMAIN_CLASS.name.like(search)).all()

    def list(self, skip: int = 0, limit: int = 1000):
        if limit:
            q = self.db.query(self.DOMAIN_CLASS).limit(limit)
        if skip:
            q = self.db.query(self.DOMAIN_CLASS).offset(skip)
        if not limit and not skip:
            return self.db.query(self.DOMAIN_CLASS).count(), self.db.query(self.DOMAIN_CLASS).all()
        return self.db.query(self.DOMAIN_CLASS).count(), q.all()

    def get_data_by_name(self, name: str = None):
        return self.db.query(self.DOMAIN_CLASS).filter(self.DOMAIN_CLASS.name == name).first()

    def get_data_by_id(self, id: int = 0):
        return self.db.query(self.DOMAIN_CLASS).filter(self.DOMAIN_CLASS.id == id).first()

    def delete(self, item):
        self.db.delete(item)
        self.db.commit()

    def update(self, item, kwargs=None, ignore_none=True):
        if kwargs:
            for attr, value in kwargs.items():
                if not (ignore_none and value is None):
                    setattr(item, attr, value)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def batch_save(self, items):
        """批量插入/保存

        :param items: 实例列表
        :return:
        """
        page_size = 1000
        page_num = len(items) // page_size

        if len(items) % page_size != 0:
            page_num = page_num + 1

        for page in range(0, page_num):
            self.db.bulk_save_objects(
                items[page * page_size: (page + 1) * page_size]
            )
        self.db.commit()
        # self.db.refresh(items)
        return items
