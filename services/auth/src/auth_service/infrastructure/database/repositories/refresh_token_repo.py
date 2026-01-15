from datetime import datetime
from typing import Optional

from .base import BaseRepository
from ..models.refresh_token import RefreshToken


class RefreshTokenRepository(BaseRepository):
    def __init__(self):
        super().__init__(RefreshToken)

    async def get_active_token(self, user_id: str, token_hash: str) -> Optional[dict]:
        """Получение активного refresh токена"""
        return await self._get_one(
            filters=[
                RefreshToken.user_id == user_id,
                RefreshToken.token_hash == token_hash,
                RefreshToken.is_revoked == False,
                RefreshToken.expires_at > datetime.now(),
            ]
        )

    async def revoke_token(self, token_id: int) -> bool:
        """Отзыв refresh токена"""
        return await self.update_by_id(
            token_id,
            {"is_revoked": True, "last_used_at": datetime.now()}
        )

    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Отзыв всех refresh токенов пользователя"""
        return await self._update_where(
            values={"is_revoked": True},
            filters=[
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,
            ]
        )

    async def update_last_used(self, token_id: int) -> bool:
        """Обновление времени последнего использования токена"""
        return await self.update_by_id(
            token_id,
            {"last_used_at": datetime.now()}
        )
