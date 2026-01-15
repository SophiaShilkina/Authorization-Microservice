from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from ..expections import DomainValidationError
from ..events import CreateRefreshSessionEvent


@dataclass
class RefreshSessionDM:
    id: UUID
    user_id: UUID
    token_hash: str
    expires_at: datetime
    revoked: bool
    _domain_events: list = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(
            cls,
            user_id: UUID,
            token_hash: str,
            expires_at: datetime,
    ) -> 'RefreshSessionDM':

        refresh_session = cls(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            revoked=False,
        )

        refresh_session.add_domain_event(
            CreateRefreshSessionEvent(
                session_id=refresh_session.id,
                user_id=refresh_session.user_id,
                expires_at=refresh_session.expires_at,
                occurred_at=datetime.now()
            )
        )

        return refresh_session

    def is_revoked(self) -> bool:
        return self.revoked

    def is_expired(self, time: datetime) -> bool:
        return time > self.expires_at

    def revoke(self) -> None:
        if self.is_revoked():
            raise DomainValidationError("Session already revoked")

        self.revoked = True

    def rotate(self, new_token_hash: str, expires_at: datetime) -> 'RefreshSessionDM':
        self.revoke()

        new_session = self.__class__.create(
            user_id=self.user_id,
            token_hash=new_token_hash,
            expires_at=expires_at,
        )

        return new_session

    def is_valid(self, time: datetime) -> bool:
        return not self.is_revoked() and not self.is_expired(time)

    def add_domain_event(self, event) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
