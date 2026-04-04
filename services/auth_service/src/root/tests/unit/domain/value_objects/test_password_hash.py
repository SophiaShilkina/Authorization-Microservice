import pytest

from root.domain.value_objects import PasswordHashVO
from root.domain.exceptions import InvalidTypeError, EmptyValueError, InvalidLengthError


@pytest.fixture
def valid_password_hash():
    return 'e234dsdom3k2kmdl3l43iwes9vjro44223m3n32kn5n2ksdo4'


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_password_hash_invalid_type(invalid_value):
    with pytest.raises(InvalidTypeError):
        PasswordHashVO(invalid_value)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_password_hash_empty_or_blank(invalid_value):
    with pytest.raises(EmptyValueError):
        PasswordHashVO(invalid_value)


def test_password_hash_min_length():
    short_password_hash = '2kmdl3l4'

    with pytest.raises(InvalidLengthError):
        PasswordHashVO(short_password_hash)


def test_password_hash_str(valid_password_hash):
    token = PasswordHashVO(valid_password_hash)

    assert str(token) == '********'


def test_password_hash_repr(valid_password_hash):
    token = PasswordHashVO(valid_password_hash)

    result = repr(token)

    assert valid_password_hash not in result
