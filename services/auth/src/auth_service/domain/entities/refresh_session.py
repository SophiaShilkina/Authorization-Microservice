from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from ..exceptions import InvariantViolation
from ..events import CreateRefreshSessionEvent, DomainEvent


@dataclass
class RefreshSessionDM:
    _id: UUID
    _user_id: UUID
    _token_hash: str
    _expires_at: datetime
    _revoked: bool
    _domain_events: list[DomainEvent] = field(default_factory=list, init=False, repr=False)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def token_hash(self) -> str:
        return self._token_hash

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    @property
    def is_revoked(self) -> bool:
        return self._revoked

    @classmethod
    def create(
            cls,
            user_id: UUID,
            token_hash: str,
            expires_at: datetime,
    ) -> 'RefreshSessionDM':

        refresh_session = cls(
            _id=uuid4(),
            _user_id=user_id,
            _token_hash=token_hash,
            _expires_at=expires_at,
            _revoked=False,
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

    def is_expired(self, time: datetime) -> bool:
        return time > self.expires_at

    def is_valid(self, time: datetime) -> bool:
        return not self.is_revoked and not self.is_expired(time)

    def revoke(self) -> None:
        if self.is_revoked:
            raise InvariantViolation('Session already revoked')
        self._revoked = True

    def rotate(
            self,
            new_token_hash: str,
            expires_at: datetime
    ) -> 'RefreshSessionDM':

        self.revoke()

        new_session = self.__class__.create(
            user_id=self.user_id,
            token_hash=new_token_hash,
            expires_at=expires_at,
        )

        return new_session

    def add_domain_event(self, event) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> list:
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events
