import pytest

from root.domain.value_objects import TokenHashVO
from root.domain.exceptions import InvalidTypeError, EmptyValueError, InvalidLengthError


@pytest.fixture
def valid_token_hash():
    return 'e234dsdom3k2kmdl3l43iwes9vjro44223m3n32kn5n2ksdo4'


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_token_hash_invalid_type(invalid_value):
    with pytest.raises(InvalidTypeError):
        TokenHashVO(invalid_value)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_token_hash_empty_or_blank(invalid_value):
    with pytest.raises(EmptyValueError):
        TokenHashVO(invalid_value)


def test_token_hash_min_length():
    short_token_hash = '2kmdl3l4'

    with pytest.raises(InvalidLengthError):
        TokenHashVO(short_token_hash)


def test_token_hash_str(valid_token_hash):
    token = TokenHashVO(valid_token_hash)

    assert str(token) == '********'


def test_token_hash_repr(valid_token_hash):
    token = TokenHashVO(valid_token_hash)

    result = repr(token)

    assert valid_token_hash not in result
