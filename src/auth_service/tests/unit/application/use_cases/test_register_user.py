import pytest
from unittest.mock import Mock

from auth_service.application.use_cases.register_user import RegisterUserUseCase
from auth_service.application.dto import RegisterUserCommand, ContextDTO
from auth_service.application.exceptions import AlreadyExists
from auth_service.domain.entities import UserDM
from auth_service.domain.value_objects import EmailVO


@pytest.fixture
def use_case(uow_mock, user_repo_mock, password_hasher_mock, email_service_mock,
             rate_limit_service_mock, clock_mock):
    return RegisterUserUseCase(
        uow=uow_mock,
        user_repo=user_repo_mock,
        password_hasher=password_hasher_mock,
        email_service=email_service_mock,
        rate_limit_service=rate_limit_service_mock,
        email_rate_limit_policy=Mock(),
        ip_rate_limit_policy=Mock(),
        clock=clock_mock
    )


@pytest.fixture
def command():
    return RegisterUserCommand(
        email='newuser@example.com',
        password='Pass_word123!',
        username='user',
        context=ContextDTO(
            ip='192.168.1.1',
            user_agent='user_agent',
        )
    )


@pytest.mark.asyncio
async def test_execute_success(use_case, command, user_repo_mock, password_hasher_mock, email_service_mock):
    result = await use_case.execute(command)

    assert result.id is not None
    assert result.email == 'newuser@example.com'
    assert result.username == 'user'

    user_repo_mock.exists_by_email.assert_called_once_with(EmailVO('newuser@example.com'))
    password_hasher_mock.get_password_hash.assert_called_once()
    user_repo_mock.create.assert_called_once()
    assert isinstance(user_repo_mock.create.call_args[0][0], UserDM)
    email_service_mock.send_verification_email.assert_called_once_with(
        email='newuser@example.com',
        username='user'
    )


@pytest.mark.asyncio
async def test_execute_email_already_exists(use_case, command, user_repo_mock):
    user_repo_mock.exists_by_email.return_value = True

    with pytest.raises(AlreadyExists):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_execute_rate_limit_enforced(use_case, command, rate_limit_service_mock):
    await use_case.execute(command)

    rate_limit_service_mock.check.assert_any_call(
        'register:email:newuser@example.com',
        use_case._email_policy
    )
    rate_limit_service_mock.check.assert_any_call(
        'register:ip:192.168.1.1',
        use_case._ip_policy
    )
