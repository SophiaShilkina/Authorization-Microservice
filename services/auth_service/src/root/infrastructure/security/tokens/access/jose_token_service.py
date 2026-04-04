from datetime import datetime, timedelta
from uuid import uuid4, UUID

from root.domain.value_objects import TokenVO
from root.application.ports import IAccessTokenService
from root.application.security.models import AccessTokenPayload
from root.infrastructure.exceptions import InvalidAccessToken

from jose import jwt, JWTError


class JoseAccessTokenService(IAccessTokenService):
    def __init__(self,
                 private_key: str,
                 public_key: str,
                 algorithm: str,
                 ttl_minutes: int):
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._ttl = ttl_minutes

    def issue(self, payload: AccessTokenPayload, now: datetime) -> TokenVO:
        exp = now + timedelta(minutes=self._ttl)
        claims = {
            "iss": "Auth Server",
            'sub': str(payload.user_id),
            'iat': int(now.timestamp()),
            'exp': int(exp.timestamp()),
            'jti': uuid4().hex,
        }

        return TokenVO(jwt.encode(claims, self._private_key, algorithm=self._algorithm))

    def verify(self, token: TokenVO) -> AccessTokenPayload:
        try:
            payload = jwt.decode(token.value, self._public_key, algorithms=[self._algorithm])
            return AccessTokenPayload(user_id=UUID(payload['sub']))
        except JWTError:
            raise InvalidAccessToken()
