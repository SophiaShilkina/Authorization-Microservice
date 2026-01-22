from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from ..value_objects import TokenHashVO, ExpiresAtVO
from ..exceptions import InvariantViolation
from ..events import CreateRefreshSessionEvent, DomainEvent


@dataclass(slots=True)
class RefreshSessionDM:
    _user_id: UUID
    _token_hash: TokenHashVO
    _expires_at: ExpiresAtVO
    _revoked: bool
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

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

        refresh_session.add_domain_event(
            CreateRefreshSessionEvent(
                user_id=refresh_session.user_id,
                expires_at=refresh_session.expires_at.value,
                occurred_at=occurred_at
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

    def add_domain_event(self, event) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
