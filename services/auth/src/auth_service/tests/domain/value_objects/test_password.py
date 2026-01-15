import pytest

from auth_service.domain.value_objects import PasswordVO
from auth_service.domain.expections import DomainValidationError


def test_valid_password():
    password = PasswordVO('ValidP@ss1')
    assert password.value == 'ValidP@ss1'


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_username_invalid_type(invalid_value):
    with pytest.raises(DomainValidationError):
        PasswordVO(invalid_value)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_username_empty_or_blank(invalid_value):
    with pytest.raises(DomainValidationError):
        PasswordVO(invalid_value)


def test_invalid_password_min_length():
    with pytest.raises(DomainValidationError):
        PasswordVO('A1@')


def test_invalid_password_max_length():
    long_password = 'A' * 65 + 'a1@'

    with pytest.raises(DomainValidationError):
        PasswordVO(long_password)


def test_password_contains_spaces():
    with pytest.raises(DomainValidationError):
        PasswordVO('With Space1@')


def test_password_missing_uppercase():
    with pytest.raises(DomainValidationError):
        PasswordVO('qwertyuiop123@')


def test_password_has_lowercase():
    with pytest.raises(DomainValidationError):
        PasswordVO('QWERTYUIOP123@')


def test_password_missing_digit():
    with pytest.raises(DomainValidationError):
        PasswordVO('NoDigits@')


def test_password_missing_special_char():
    with pytest.raises(DomainValidationError):
        PasswordVO("NoSpecial123")


def test_common_password():
    with pytest.raises(DomainValidationError):
        PasswordVO('password1@Q')


def test_password_string_representation():
    password = PasswordVO('Secret@123')
    assert str(password) == '********'
    assert '********' in repr(password)
