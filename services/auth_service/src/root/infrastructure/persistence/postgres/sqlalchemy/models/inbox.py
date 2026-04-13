
from .base import BaseORM
from .mixins import IdUUIDPKMixin, CUDateTimeMixin


class InboxORM(IdUUIDPKMixin, CUDateTimeMixin, BaseORM):


    __tablename__ = 'inbox'
    __table_args__ = (
        {'schema': 'public'}
    )
