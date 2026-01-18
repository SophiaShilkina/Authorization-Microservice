from datetime import datetime, timedelta, timezone

import pytest

from auth_service.domain.value_objects import AccessTokenVO, ExpiresAtVO
from auth_service.domain.exceptions import InvalidTypeError, EmptyValueError


@pytest.fixture
def expires_at_feature():
    return ExpiresAtVO(datetime.now(timezone.utc) + timedelta(hours=1))

@pytest.fixture
def valid_token_value():
    return 'LaZniFO64ujuEkgCB7cTHyDZncwdLrelwKpOK0fD1Qp7zBO27sZ8yuiIOCKuIoVM'


def test_access_token_valid(valid_token_value, expires_at_feature):
    token = AccessTokenVO(
        value=valid_token_value,
        expires_at=expires_at_feature
    )

    assert token.value
    assert token.expires_at == expires_at_feature


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_access_token_invalid_type(invalid_value, expires_at_feature):
    with pytest.raises(InvalidTypeError):
        AccessTokenVO(invalid_value, expires_at_feature)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_access_token_empty_or_blank(invalid_value, expires_at_feature):
    with pytest.raises(EmptyValueError):
        AccessTokenVO(invalid_value, expires_at_feature)


def test_access_token_str_masked(valid_token_value, expires_at_feature):
    token = AccessTokenVO(
        value=valid_token_value,
        expires_at=expires_at_feature
    )

    str_repr = str(token)
    assert "LaZn" in str_repr
    assert "..." in str_repr
    assert "IoVM" in str_repr
    assert len(str_repr) < len(token.value)


def test_access_token_str_short_masked(expires_at_feature):
    token = AccessTokenVO(
        value="short",
        expires_at=expires_at_feature
    )

    assert str(token) == "***"
