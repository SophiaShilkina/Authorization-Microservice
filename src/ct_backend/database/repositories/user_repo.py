from .base import BaseRepository
from ..models.user import User

from sqlalchemy import or_


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, user_title: str):
        return await self._get_one(
            filters=[or_(
                User.email == user_title,
                User.username == user_title
            )],
            columns=[User.id]
        )


user_repo = UserRepository()