from uuid import uuid4
from datetime import timedelta

import pytest
from unittest.mock import Mock

from auth_service.domain.entities import UserDM
from auth_service.domain.value_objects import EmailVO, PasswordHashVO
from auth_service.application.use_cases.login_user import LoginUserUseCase
from auth_service.application.dto import LoginUserCommand, ContextDTO
from auth_service.application.security.policies import PasswordPolicy
from auth_service.application.exceptions import AuthenticationFailed


@pytest.fixture
def use_case(uow_mock, user_repo_mock, refresh_session_repo_mock, password_hasher_mock, refresh_token_service_mock,
             access_token_service_mock, rate_limit_service_mock, clock_mock):
    return LoginUserUseCase(
        uow=uow_mock,
        user_repo=user_repo_mock,
        refresh_session_repo=refresh_session_repo_mock,
        password_hasher=password_hasher_mock,
        refresh_token_service=refresh_token_service_mock,
        access_token_service=access_token_service_mock,
        rate_limit_service=rate_limit_service_mock,
        token_policy=Mock(refresh_ttl=timedelta(days=7), access_ttl=timedelta(hours=1)),
        email_rate_limit_policy=Mock(),
        ip_rate_limit_policy=Mock(),
        clock=clock_mock
    )


@pytest.fixture
def context():
    return ContextDTO(
        ip='127.0.0.1',
        user_agent='user_agent',
    )


@pytest.mark.asyncio
async def test_execute_success(use_case, user_repo_mock, password_hasher_mock,
                               access_token_service_mock, refresh_session_repo_mock, context):
    user = Mock(
        spec=UserDM,
        id=uuid4(),
        email=EmailVO('test@example.com'),
        password_hash=PasswordHashVO('password_hash_jro44223m3n32kn5n2ksdo4e234dsdom3k2kmdl3l43iwes9v'),
        ensure_can_login=Mock()
    )
    user_repo_mock.get_by_email.return_value = user

    command = LoginUserCommand(
        email='test@example.com',
        password='Pass_word123!',
        context=context
    )

    result = await use_case.execute(command)

    assert result.access_token == 'access_token_om3k2kmdsdjro4.4223m3n3dl3l43iw.n2ksdo4e234es9v2kn5'
    assert result.refresh_token == 'refresh_token_n5n2ksdo4edsdom3k2kmjro44223m3n3dl3l43iwes9v2k234'

    user_repo_mock.get_by_email.assert_called_once()
    password_hasher_mock.verify.assert_called_once_with(PasswordPolicy('Pass_word123!'), user.password_hash)
    user.ensure_can_login.assert_called_once()
    refresh_session_repo_mock.create.assert_called_once()
    access_token_service_mock.issue.assert_called_once()


@pytest.mark.asyncio
async def test_execute_user_not_found(use_case, password_hasher_mock, context):
    command = LoginUserCommand(
        email='nonexistent@example.com',
        password='Pass_word123!',
        context=context
    )

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)

    password_hasher_mock.dummy_verify.assert_called_once_with(PasswordPolicy('Pass_word123!'))


@pytest.mark.asyncio
async def test_execute_invalid_password(use_case, user_repo_mock, password_hasher_mock, context):
    user = Mock(
        spec=UserDM,
        password_hash=PasswordHashVO('password_hash_jro44223m3n32kn5n2ksdo4e234dsdom3k2kmdl3l43iwes9v')
    )
    user_repo_mock.get_by_email.return_value = user
    password_hasher_mock.verify.return_value = False

    command = LoginUserCommand(
        email='test@example.com',
        password='WrongPass_word!1',
        context=context
    )

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)

    password_hasher_mock.verify.assert_called_once_with(PasswordPolicy('WrongPass_word!1'), user.password_hash)


@pytest.mark.asyncio
async def test_execute_user_blocked(use_case, user_repo_mock, context):
    user = Mock(spec=UserDM)
    user_repo_mock.get_by_email.return_value = user
    user.ensure_can_login.side_effect = AuthenticationFailed('The user is blocked or deactivate')

    command = LoginUserCommand(
        email='blocked@example.com',
        password='Pass_word123!',
        context=context
    )

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_execute_rate_limit_called(use_case, user_repo_mock, rate_limit_service_mock, context):
    user = Mock(spec=UserDM)
    user_repo_mock.get_by_email.return_value = user

    command = LoginUserCommand(
        email='test@example.com',
        password='Pass_word123!',
        context=context
    )

    await use_case.execute(command)

    rate_limit_service_mock.check.assert_any_call(
        'login:email:test@example.com',
        use_case._email_policy
    )
    rate_limit_service_mock.check.assert_any_call(
        'login:ip:127.0.0.1',
        use_case._ip_policy
    )
