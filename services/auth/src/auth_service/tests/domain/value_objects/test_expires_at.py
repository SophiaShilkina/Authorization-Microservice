from datetime import datetime, timedelta, timezone

import pytest

from auth_service.domain.value_objects import ExpiresAtVO
from auth_service.domain.exceptions import InvalidTypeError, InvariantViolation


@pytest.fixture
def now():
    return datetime.now(timezone.utc)


@pytest.fixture
def expires_at_feature():
    return datetime.now(timezone.utc) + timedelta(hours=1)


@pytest.fixture
def expires_at_past():
    return datetime.now(timezone.utc) - timedelta(hours=1)


def test_valid_expires_at(expires_at_feature):
    expires_at = ExpiresAtVO(expires_at_feature)

    assert expires_at.value == expires_at_feature


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_expires_at_invalid_type(invalid_value):
    with pytest.raises(InvalidTypeError):
        ExpiresAtVO(invalid_value)  # type: ignore


def test_reject_datetime_without_tz():
    naive_dt = datetime.now()

    with pytest.raises(InvalidTypeError):
        ExpiresAtVO(naive_dt)


def test_is_expired_with_future_time(now, expires_at_feature):
    expires_at = ExpiresAtVO(expires_at_feature)

    assert expires_at.is_expired(now) is False
    assert expires_at.is_active(now) is True


def test_is_expired_with_past_time(now, expires_at_past):
    expires_at = ExpiresAtVO(expires_at_past)

    assert expires_at.is_expired(now) is True
    assert expires_at.is_active(now) is False


def test_is_expired_with_same_time(now):
    expires_at = ExpiresAtVO(now)

    assert expires_at.is_expired(now) is True
    assert expires_at.is_active(now) is False


def test_is_expired_rejects_naive_datetime(now):
    expires_at = ExpiresAtVO(now)
    naive_now = datetime.now()

    with pytest.raises(InvalidTypeError):
        expires_at.is_expired(naive_now)


def test_is_expired_rejects_different_timezone(now):
    expires_at = ExpiresAtVO(now)

    msk_time = datetime.now(timezone(timedelta(hours=3)))

    with pytest.raises(InvariantViolation):
        expires_at.is_expired(msk_time)

def test_string_representation():
    expires_at = datetime(2024, 1, 20, 12, 30, 45, tzinfo=timezone.utc)
    expires_at_vo = ExpiresAtVO(expires_at)

    assert str(expires_at_vo) == "2024-01-20T12:30:45+00:00"
