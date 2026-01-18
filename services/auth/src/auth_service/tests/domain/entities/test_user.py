from uuid import UUID, uuid4
from datetime import datetime

import pytest

from auth_service.domain.entities import UserDM
from auth_service.domain.value_objects import EmailVO, UsernameVO, PasswordHashVO
from auth_service.domain.exceptions import InvariantViolation, BusinessRuleViolation
from auth_service.domain.events import UserRegisteredEvent


@pytest.fixture
def valid_email():
    return EmailVO('test@example.com')


@pytest.fixture
def valid_username():
    return UsernameVO('test_user')


@pytest.fixture
def valid_password_hash():
    return PasswordHashVO('e234dsdom3k2kmdl3l43iwes9vjro44223m3n32kn5n2ksdo4')


@pytest.fixture
def registered_user(valid_email, valid_username, valid_password_hash):
    return UserDM.register(
        email=valid_email,
        username=valid_username,
        password_hash=valid_password_hash
    )


def test_cannot_change_fields_directly(registered_user):
    with pytest.raises(AttributeError):
        registered_user.id = uuid4()

    with pytest.raises(AttributeError):
        registered_user.email = EmailVO('new@example.com')

    with pytest.raises(AttributeError):
        registered_user.username = UsernameVO('new_username')

    with pytest.raises(AttributeError):
        registered_user.password_hash = PasswordHashVO('new_password_hash_dl3l43iwes9vjro44223m3n32kn5n2ksdo4')

    with pytest.raises(AttributeError):
        registered_user.active = False

    with pytest.raises(AttributeError):
        registered_user.blocked = True

    with pytest.raises(AttributeError):
        registered_user.verified = True


def test_user_register_success(valid_email, valid_username, valid_password_hash):
    user = UserDM.register(
        email=valid_email,
        username=valid_username,
        password_hash=valid_password_hash
    )

    assert isinstance(user.id, UUID)
    assert user.email == valid_email
    assert user.username == valid_username
    assert user.password_hash == valid_password_hash
    assert user.is_active is True
    assert user.is_verified is False
    assert user.is_blocked is False


def test_activation_logic_returns_correct_value(registered_user):
    assert registered_user.is_active is True

    registered_user.deactivate()
    assert registered_user.is_active is False

    registered_user.activate()
    assert registered_user.is_active is True


def test_activation_logic_raises_error(registered_user):
    with pytest.raises(InvariantViolation):
        registered_user.activate()


def test_deactivation_logic_raises_error(registered_user):
    registered_user.deactivate()

    with pytest.raises(InvariantViolation):
        registered_user.deactivate()


def test_block_logic_returns_correct_value(registered_user):
    assert registered_user.is_blocked is False

    registered_user.block()
    assert registered_user.is_blocked is True

    registered_user.unblock()
    assert registered_user.is_blocked is False


def test_unblock_logic_raises_error(registered_user):
    with pytest.raises(InvariantViolation):
        registered_user.unblock()


def test_block_logic_raises_error(registered_user):
    registered_user.block()

    with pytest.raises(InvariantViolation):
        registered_user.block()


def test_verify_logic_returns_correct_value(registered_user):
    assert registered_user.is_verified is False

    registered_user.verify()
    assert registered_user.is_verified is True


def test_verify_logic_raises_error(registered_user):
    registered_user.verify()

    with pytest.raises(InvariantViolation):
        registered_user.verify()


def test_blocked_user_cannot_login(registered_user):
    registered_user.block()

    with pytest.raises(InvariantViolation):
        registered_user.ensure_can_login()


def test_inactive_user_cannot_login(registered_user):
    registered_user.deactivate()

    with pytest.raises(InvariantViolation):
        registered_user.ensure_can_login()


def test_blocked_and_inactive_user_cannot_login(registered_user):
    registered_user.block()
    registered_user.deactivate()

    with pytest.raises(InvariantViolation):
        registered_user.ensure_can_login()


def test_change_email_success(registered_user):
    new_email = EmailVO("new@example.com")

    registered_user.change_email(new_email)
    assert registered_user.email == new_email


def test_change_email_to_same_email_raises_error(registered_user, valid_email):
    with pytest.raises(BusinessRuleViolation):
        registered_user.change_email(valid_email)


def test_change_username_success(registered_user):
    new_username = UsernameVO('new_username')

    registered_user.change_username(new_username)
    assert registered_user.username == new_username


def test_change_username_to_same_username_raises_error(registered_user, valid_username):
    with pytest.raises(BusinessRuleViolation):
        registered_user.change_username(valid_username)


def test_change_password_hash_success(registered_user):
    new_hash = PasswordHashVO('new_password_hash_dl3l43iwes9vjro44223m3n32kn5n2ksdo4')

    registered_user.change_password_hash(new_hash)
    assert registered_user.password_hash == new_hash


def test_user_register_generate_domain_event(valid_email, valid_username, valid_password_hash):
    user = UserDM.register(
        email=valid_email,
        username=valid_username,
        password_hash=valid_password_hash
    )

    events = user.pull_domain_events()
    assert len(events) == 1

    event = events[0]
    assert isinstance(event, UserRegisteredEvent)
    assert event.user_id == user.id
    assert event.email == user.email.value
    assert event.username == user.username.value
    assert isinstance(event.occurred_at, datetime)


def test_domain_events_are_cleared_after_pull(registered_user):
    events = registered_user.pull_domain_events()

    assert len(events) == 1
    assert len(registered_user._domain_events) == 0
