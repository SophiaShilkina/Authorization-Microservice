from datetime import datetime, timedelta
from uuid import uuid4, UUID

from auth_service.application.ports import IAccessTokenService
from auth_service.application.security.models import AccessTokenPayload, AccessToken
from auth_service.infrastructure.expections import InvalidAccessToken

from jose import jwt, JWTError


class JoseAccessTokenService(IAccessTokenService):
    def __init__(self,
                 secret_key: str,
                 algorithm: str,
                 ttl_minutes: int):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._ttl = ttl_minutes

    def issue(self, payload: AccessTokenPayload, now: datetime) -> AccessToken:
        exp = now + timedelta(minutes=self._ttl)
        claims = {
            'sub': str(payload.user_id),
            'iat': int(now.timestamp()),
            'exp': int(exp.timestamp()),
            'jti': uuid4().hex,
        }

        return AccessToken(
            token=jwt.encode(claims, self._secret_key, algorithm=self._algorithm),
            expires_at=exp,
        )

    def verify(self, token: AccessToken) -> AccessTokenPayload:
        try:
            payload = jwt.decode(token.token, self._secret_key, algorithms=[self._algorithm])
            return AccessTokenPayload(user_id=UUID(payload['sub']))
        except JWTError:
            raise InvalidAccessToken()
