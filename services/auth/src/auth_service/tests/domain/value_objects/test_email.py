import pytest

from auth_service.domain.value_objects import EmailVO
from auth_service.domain.expections import DomainValidationError


def test_email_is_trimmed():
    email = EmailVO("  test@example.com  ")
    assert email.value == "test@example.com"


def test_email_is_lowercased():
    email = EmailVO("Test@Example.COM")
    assert email.value == "test@example.com"


@pytest.mark.parametrize("valid_email", [
    "simple@example.com",
    "very.common@example.com",
    "disposable.style.email.with+symbol@example.com",
    "other.email-with-dash@example.com",
    "fully-qualified-domain@example.com",
    "user.name+tag+sorting@example.com",
    "x@example.com",
    "example-indeed@strange-example.com",
    "example@s.example",
    "user%example.com@example.org",
    "user-@example.org",
])
def test_valid_email(valid_email):
    email = EmailVO(valid_email)
    assert email.value == valid_email


@pytest.mark.parametrize('invalid_email', [
    'plainaddress',
    '@missing-local.com',
    'missing-at-domain.com',
    'missing-tld@domain',
    'abc.example.com',
    'a@b@c@example.com',
    'あいうえお@example.com',
    'email@123.123.123.123',
    'email@[123.123.123.123]',
    'just\'not\'right@example.com',
    'this is\'not\\allowed@example.com',
    'this\\ still\\\'not\\\\allowed@example.com',
    'email@example.c'
])
def test_invalid_email(invalid_email):
    with pytest.raises(DomainValidationError):
        EmailVO(invalid_email)


@pytest.mark.parametrize('invalid_email', [
    None,
    123,
    '',
    ' ',
])
def test_invalid_email_type_or_empty(invalid_email):
    with pytest.raises(DomainValidationError):
        EmailVO(invalid_email)


@pytest.mark.parametrize('invalid_email', [
    'john..doe@example.com',
    'john.doe@example..com',
    'email@-example.com',
    'email@example-.com',
])
def test_invalid_email_structure(invalid_email):
    with pytest.raises(DomainValidationError):
        EmailVO(invalid_email)
