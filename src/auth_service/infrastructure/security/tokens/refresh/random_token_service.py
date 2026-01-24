import secrets
import hashlib

from auth_service.domain.value_objects import TokenVO, TokenHashVO
from auth_service.application.ports import IRefreshTokenService


class RandomRefreshTokenService(IRefreshTokenService):
    def generate(self) -> tuple[TokenVO, TokenHashVO]:
        token = TokenVO(secrets.token_urlsafe(32))
        return token, self.hash(token)

    @staticmethod
    def hash(raw_token: TokenVO) -> TokenHashVO:
        return TokenHashVO(
            hashlib.sha256(raw_token.value.encode()).hexdigest()
        )
