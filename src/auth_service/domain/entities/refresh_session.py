from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from .base import BaseDM
from ..value_objects import TokenHashVO, ExpiresAtVO
from ..exceptions import InvariantViolation
from ..events import CreateRefreshSessionEvent


@dataclass(slots=True)
class RefreshSessionDM(BaseDM):
    _user_id: UUID
    _token_hash: TokenHashVO
    _expires_at: ExpiresAtVO
    _revoked: bool

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def token_hash(self) -> TokenHashVO:
        return self._token_hash

    @property
    def expires_at(self) -> ExpiresAtVO:
        return self._expires_at

    @property
    def is_revoked(self) -> bool:
        return self._revoked

    @classmethod
    def create(
            cls,
            user_id: UUID,
            token_hash: TokenHashVO,
            expires_at: ExpiresAtVO,
            occurred_at: datetime
    ) -> 'RefreshSessionDM':

        refresh_session = cls(
            _user_id=user_id,
            _token_hash=token_hash,
            _expires_at=expires_at,
            _revoked=False,
        )

        refresh_session._add_domain_event(
            CreateRefreshSessionEvent(
                event_id=uuid4(),
                event_type='auth.refresh_session.create',
                user_id=refresh_session.user_id,
                token_hash=refresh_session.token_hash.value,
                expires_at=refresh_session.expires_at.value,
                occurred_at=occurred_at,
            )
        )

        return refresh_session

    @classmethod
    def hydrate(
            cls,
            *,
            user_id: UUID,
            token_hash: TokenHashVO,
            expires_at: ExpiresAtVO,
            revoked: bool,
    ) -> 'RefreshSessionDM':
        return cls(
            _user_id=user_id,
            _token_hash=token_hash,
            _expires_at=expires_at,
            _revoked=revoked,
        )

    def is_expired(self, time: datetime) -> bool:
        return self.expires_at.is_expired(time)

    def is_valid(self, time: datetime) -> bool:
        return not self.is_revoked and not self.is_expired(time)

    def revoke(self) -> None:
        if self.is_revoked:
            raise InvariantViolation('Session already revoked')
        self._revoked = True

    def rotate(
            self,
            new_token_hash: TokenHashVO,
            expires_at: ExpiresAtVO,
            occurred_at: datetime
    ) -> 'RefreshSessionDM':

        self.revoke()

        new_session = self.__class__.create(
            user_id=self.user_id,
            token_hash=new_token_hash,
            expires_at=expires_at,
            occurred_at=occurred_at,
        )

        return new_session
