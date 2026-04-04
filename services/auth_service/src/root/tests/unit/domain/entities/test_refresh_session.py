from uuid import uuid4
from datetime import datetime, timezone, timedelta

import pytest

from root.domain.entities import RefreshSessionDM
from root.domain.value_objects import TokenHashVO, ExpiresAtVO
from root.domain.exceptions import InvariantViolation
from root.domain.events import RefreshSessionCreatedEvent


@pytest.fixture
def valid_user_id():
    return uuid4()


@pytest.fixture
def valid_token_hash():
    return TokenHashVO('e234dsdom3k2kmdl3l43iwes9vjro44223m3n32kn5n2ksdo4')


@pytest.fixture
def expires_at_future():
    return ExpiresAtVO(datetime.now(timezone.utc) + timedelta(hours=1))


@pytest.fixture
def expires_at_past():
    return ExpiresAtVO(datetime.now(timezone.utc) - timedelta(hours=1))


@pytest.fixture
def now_datetime():
    return datetime.now(timezone.utc)


@pytest.fixture
def expires_at_future_datetime():
    return datetime.now(timezone.utc) + timedelta(minutes=30)


@pytest.fixture
def valid_refresh_session(valid_user_id, valid_token_hash, expires_at_future, now_datetime):
    return RefreshSessionDM.create(
        user_id=valid_user_id,
        token_hash=valid_token_hash,
        expires_at=expires_at_future,
        occurred_at=now_datetime
    )


def test_cannot_change_fields_directly(valid_refresh_session):
    with pytest.raises(AttributeError):
        valid_refresh_session.id = uuid4()

    with pytest.raises(AttributeError):
        valid_refresh_session.user_id = uuid4()

    with pytest.raises(AttributeError):
        valid_refresh_session.token_hash = TokenHashVO('jro44223m3n32kn5n2ksdo4e234dsdom3k2kmdl3l43iwes9v')

    with pytest.raises(AttributeError):
        valid_refresh_session.expires_at = ExpiresAtVO(datetime.now(timezone.utc) + timedelta(hours=2))

    with pytest.raises(AttributeError):
        valid_refresh_session.is_revoked = True


def test_create_refresh_session(valid_user_id, valid_token_hash, expires_at_future, now_datetime):
    session = RefreshSessionDM.create(
        user_id=valid_user_id,
        token_hash=valid_token_hash,
        expires_at=expires_at_future,
        occurred_at=now_datetime
    )

    assert session.user_id == valid_user_id
    assert session.token_hash == valid_token_hash
    assert session.expires_at == expires_at_future
    assert session.is_revoked is False


def test_is_expired_future_time(valid_refresh_session, expires_at_future_datetime):
    assert valid_refresh_session.is_expired(expires_at_future_datetime) is False


def test_is_expired_past_time(valid_user_id, valid_token_hash, expires_at_past, now_datetime):
    session = RefreshSessionDM.create(
        user_id=valid_user_id,
        token_hash=valid_token_hash,
        expires_at=expires_at_past,
        occurred_at=now_datetime,
    )

    assert session.is_expired(now_datetime) is True


def test_is_valid_active_session(valid_refresh_session, expires_at_future_datetime):
    assert valid_refresh_session.is_valid(expires_at_future_datetime) is True


def test_is_valid_expired_session(valid_user_id, valid_token_hash, expires_at_past, now_datetime):
    session = RefreshSessionDM.create(
        user_id=valid_user_id,
        token_hash=valid_token_hash,
        expires_at=expires_at_past,
        occurred_at=now_datetime,
    )

    assert session.is_valid(now_datetime) is False


def test_revoke_active_session(valid_refresh_session):
    valid_refresh_session.revoke()
    assert valid_refresh_session.is_revoked is True


def test_revoke_already_revoked_session(valid_refresh_session):
    valid_refresh_session.revoke()

    with pytest.raises(InvariantViolation):
        valid_refresh_session.revoke()


def test_is_valid_revoked_session(valid_refresh_session, expires_at_future_datetime):
    valid_refresh_session.revoke()
    assert valid_refresh_session.is_valid(expires_at_future_datetime) is False


def test_rotate_session(valid_refresh_session, now_datetime):
    new_token_hash = TokenHashVO('new_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v')
    new_expires_at = ExpiresAtVO(datetime.now(timezone.utc) + timedelta(hours=2))

    new_session = valid_refresh_session.rotate(
        new_token_hash=new_token_hash,
        expires_at=new_expires_at,
        occurred_at=now_datetime,
    )

    assert valid_refresh_session.is_revoked is True
    assert new_session.user_id == valid_refresh_session.user_id
    assert new_session.token_hash == new_token_hash
    assert new_session.expires_at == new_expires_at
    assert new_session.is_revoked is False


def test_create_generates_domain_event(valid_refresh_session):
    events = valid_refresh_session.pull_domain_events()
    assert len(events) == 1

    event = events[0]
    assert isinstance(event, RefreshSessionCreatedEvent)
    assert event.user_id == valid_refresh_session.user_id


def test_domain_events_are_cleared(valid_refresh_session):
    events = valid_refresh_session.pull_domain_events()
    assert len(events) == 1

    events_after = valid_refresh_session.pull_domain_events()
    assert len(events_after) == 0
