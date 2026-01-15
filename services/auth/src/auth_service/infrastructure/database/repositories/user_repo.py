from .base import BaseRepository
from ..models.user import User
from .dto import UserAllDTO


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_id_by_email(self, email: str):
        return await self._get_one(
            filters=[
                User.email == email,
            ],
            columns=[User.id]
        )

    async def get_all_by_email(self, email: str) -> UserAllDTO | None:
        row = await self._get_one(
            filters=[
                User.email == email,
            ]
        )
        if not row:
            return None

        return UserAllDTO(
            id=row["id"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            role=row["role"],
            is_active=row["is_active"],
            is_verified=row["is_verified"],
            is_blocked=row["is_blocked"],
        )
