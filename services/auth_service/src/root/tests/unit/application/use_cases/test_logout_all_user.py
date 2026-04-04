import pytest
from unittest.mock import Mock

from root.application.dto import LogoutAllUserCommand
from root.application.use_cases.logout_all_user import LogoutAllUserUseCase


@pytest.fixture
def use_case(uow_mock, refresh_session_repo_mock, access_token_service_mock, rate_limit_service_mock, clock_mock):
    return LogoutAllUserUseCase(
        uow=uow_mock,
        refresh_session_repo=refresh_session_repo_mock,
        access_token_service=access_token_service_mock,
        rate_limit_service=rate_limit_service_mock,
        user_id_rate_limit_policy=Mock(),
        clock=clock_mock,
    )


@pytest.fixture
def command():
    return LogoutAllUserCommand(
        access_token='valid_access_token',
    )


@pytest.mark.asyncio
async def test_execute_success(use_case, command, refresh_session_repo_mock, access_token_service_mock):
    refresh_session_repo_mock.revoke_all_by_user_id.return_value = 3

    result = await use_case.execute(command)

    assert result.revoked_sessions == 3

    access_token_service_mock.verify.assert_called_once()
    refresh_session_repo_mock.revoke_all_by_user_id.assert_called_once_with('user-123')


@pytest.mark.asyncio
async def test_execute_rate_limit_enforced(use_case, command, rate_limit_service_mock):
    await use_case.execute(command)

    rate_limit_service_mock.check.assert_called_once_with(
        'logout_all:user_id:user-123',
        use_case._user_id_policy
    )
