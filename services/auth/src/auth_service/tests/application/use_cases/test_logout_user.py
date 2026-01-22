import pytest
from unittest.mock import Mock

from auth_service.application.dto import LogoutUserCommand
from auth_service.application.use_cases.logout_user import LogoutUserUseCase
from auth_service.domain.entities import RefreshSessionDM
from auth_service.application.exceptions import AuthenticationFailed, TokenExpired


@pytest.fixture
def use_case(refresh_session_repo_mock, token_service_mock, clock_mock):
    return LogoutUserUseCase(
        refresh_session_repo=refresh_session_repo_mock,
        token_service=token_service_mock,
        clock=clock_mock
    )


@pytest.fixture
def command():
    return LogoutUserCommand(refresh_token='refresh_token_n5n2ksdo4edsdom3k2kmjro44223m3n3dl3l43iwes9v2k234')


@pytest.mark.asyncio
async def test_execute_success(use_case, command, refresh_session_repo_mock):
    session = Mock(
        spec=RefreshSessionDM,
        is_expired=Mock(return_value=False),
        revoke=Mock()
    )
    refresh_session_repo_mock.get_by_hash.return_value = session

    await use_case.execute(command)

    refresh_session_repo_mock.get_by_hash.assert_called_once_with('refresh_token_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v')
    session.revoke.assert_called_once()
    refresh_session_repo_mock.update.assert_called_once_with(session)


@pytest.mark.asyncio
async def test_execute_session_not_found(use_case, command, refresh_session_repo_mock):
    refresh_session_repo_mock.get_by_hash.return_value = None

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_execute_expired_token(use_case, command, refresh_session_repo_mock):
    session = Mock(spec=RefreshSessionDM, is_expired=Mock(return_value=True))
    refresh_session_repo_mock.get_by_hash.return_value = session

    with pytest.raises(TokenExpired):
        await use_case.execute(command)
