import secrets
import hashlib

from auth_service.domain.value_objects import TokenVO, TokenHashVO


class RandomTokenService:
    def generate(self) -> tuple[TokenVO, TokenHashVO]:
        token = TokenVO(secrets.token_urlsafe(32))
        return token, self.hash(token)

    @staticmethod
    def hash(token: TokenVO) -> TokenHashVO:
        return TokenHashVO(
            hashlib.sha256(token.value.encode()).hexdigest()
        )
