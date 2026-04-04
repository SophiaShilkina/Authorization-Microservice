import pytest

from root.domain.value_objects import TokenVO
from root.domain.exceptions import InvalidTypeError, EmptyValueError


@pytest.fixture
def valid_token_value():
    return 'LaZniFO64ujuEkgCB7cTHyDZncwdLrelwKpOK0fD1Qp7zBO27sZ8yuiIOCKuIoVM'


def test_token_valid(valid_token_value):
    token = TokenVO(valid_token_value)
    assert token.value


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_access_token_invalid_type(invalid_value):
    with pytest.raises(InvalidTypeError):
        TokenVO(invalid_value)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_access_token_empty_or_blank(invalid_value):
    with pytest.raises(EmptyValueError):
        TokenVO(invalid_value)


def test_access_token_str_masked(valid_token_value):
    token = TokenVO(valid_token_value)

    str_repr = str(token)
    assert "LaZn" in str_repr
    assert "..." in str_repr
    assert "IoVM" in str_repr
    assert len(str_repr) < len(token.value)


def test_access_token_str_short_masked():
    token = TokenVO('short',)
    assert str(token) == "***"
