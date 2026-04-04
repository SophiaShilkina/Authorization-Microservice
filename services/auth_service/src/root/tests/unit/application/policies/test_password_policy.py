import pytest

from root.application.security.policies import PasswordPolicy
from root.application.exceptions import InvalidLengthError, InvalidFormatError, InvalidTypeError, EmptyValueError


def test_valid_password():
    password = PasswordPolicy('ValidP@ss1')
    assert password.value == 'ValidP@ss1'


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_password_invalid_type(invalid_value):
    with pytest.raises(InvalidTypeError):
        PasswordPolicy(invalid_value)  # type: ignore


def test_empty_password():
    with pytest.raises(EmptyValueError):
        PasswordPolicy('')


def test_password_contains_spaces():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy('With Space1@')


def test_invalid_password_min_length():
    with pytest.raises(InvalidLengthError):
        PasswordPolicy('A1@')


def test_invalid_password_max_length():
    long_password = 'A' * 65 + 'a1@'

    with pytest.raises(InvalidLengthError):
        PasswordPolicy(long_password)


def test_password_missing_uppercase():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy('qwertyuiop123@')


def test_password_has_lowercase():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy('QWERTYUIOP123@')


def test_password_missing_digit():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy('NoDigits@')


def test_password_missing_special_char():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy("NoSpecial123")


def test_common_password():
    with pytest.raises(InvalidFormatError):
        PasswordPolicy('password1@Q')


def test_password_string_representation():
    password = PasswordPolicy('Secret@123')
    assert str(password) == '********'
    assert '********' in repr(password)
