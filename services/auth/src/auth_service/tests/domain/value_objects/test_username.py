import pytest

from auth_service.domain.value_objects import UsernameVO
from auth_service.domain.expections import DomainValidationError


@pytest.mark.parametrize('valid_username', [
    'user',
    'user_doe',
    'user-doe',
    'us3r_d03',
    'abc',
    'a' * 30, 
    'User123',
    'u_s_e_r',
    'test-user-01',
    'simp_us-01',
])
def test_valid_username(valid_username):
    username = UsernameVO(valid_username)
    assert username.value == valid_username


@pytest.mark.parametrize('invalid_value', [None, 123])
def test_username_invalid_type(invalid_value):
    with pytest.raises(DomainValidationError):
        UsernameVO(invalid_value)  # type: ignore


@pytest.mark.parametrize('invalid_value', ['', ' '])
def test_username_empty_or_blank(invalid_value):
    with pytest.raises(DomainValidationError):
        UsernameVO(invalid_value)


def test_invalid_min_length():
    with pytest.raises(DomainValidationError):
        UsernameVO('us')


def test_invalid_max_length():
    long_username = 'a' * 32

    with pytest.raises(DomainValidationError):
        UsernameVO(long_username)


@pytest.mark.parametrize('test_cases', [
    '___', '---', '_-_', '-_-', '__-', '--_'
])
def test_username_only_special_chars(test_cases):
    with pytest.raises(DomainValidationError):
        UsernameVO(test_cases)


@pytest.mark.parametrize('test_cases', [
    '_username', 'username_', '-username-', '-username_', '_-username_-'
])
def test_username_starts_and_ends_with_special_char(test_cases):
    with pytest.raises(DomainValidationError):
        UsernameVO(test_cases)


def test_invalid_username_pattern():
    with pytest.raises(DomainValidationError):
        UsernameVO('us@1234#')
