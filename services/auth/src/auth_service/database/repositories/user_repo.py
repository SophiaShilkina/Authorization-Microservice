from .base import BaseRepository
from ..models.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, email: str):
        return await self._get_one(
            filters=[
                User.email == email,
            ],
            columns=[User.id]
        )


user_repo = UserRepository()
