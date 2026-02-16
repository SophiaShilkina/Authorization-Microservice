from datetime import timedelta

import pytest
from unittest.mock import Mock

from auth_service.application.use_cases.refresh_token import RefreshTokenUseCase
from auth_service.application.dto import RefreshTokenCommand
from auth_service.application.exceptions import AuthenticationFailed
from auth_service.domain.entities import RefreshSessionDM


@pytest.fixture
def use_case(uow_mock, refresh_session_repo_mock, access_token_service_mock, refresh_token_service_mock,
             rate_limit_service_mock, clock_mock):
    return RefreshTokenUseCase(
        uow=uow_mock,
        refresh_session_repo=refresh_session_repo_mock,
        access_token_service=access_token_service_mock,
        refresh_token_service=refresh_token_service_mock,
        rate_limit_service=rate_limit_service_mock,
        token_policy=Mock(refresh_ttl=timedelta(days=7), access_ttl=timedelta(hours=1)),
        token_rate_limit_policy=Mock(),
        user_id_rate_limit_policy=Mock(),
        clock=clock_mock
    )


@pytest.fixture
def session():
    return Mock(
        spec=RefreshSessionDM,
        user_id='user-123',
        is_valid=Mock(return_value=True),
        rotate=Mock(return_value=Mock())
    )


@pytest.fixture
def command():
    return RefreshTokenCommand(
        refresh_token='refresh_token_n5n2ksdo4edsdom3k2kmjro44223m3n3dl3l43iwes9v2k234'
    )


@pytest.mark.asyncio
async def test_execute_success(use_case, session, command, refresh_session_repo_mock,
                               refresh_token_service_mock, access_token_service_mock):
    refresh_session_repo_mock.get_by_hash.return_value = session

    result = await use_case.execute(command)

    assert result.access_token == 'access_token_om3k2kmdsdjro4.4223m3n3dl3l43iw.n2ksdo4e234es9v2kn5'
    assert result.refresh_token == 'refresh_token_n5n2ksdo4edsdom3k2kmjro44223m3n3dl3l43iwes9v2k234'

    refresh_token_service_mock.hash.assert_called_once()
    call_arg = refresh_session_repo_mock.get_by_hash.call_args[0][0]
    assert call_arg.value == 'refresh_token_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v'
    session.rotate.assert_called_once()
    refresh_session_repo_mock.update.assert_called_once_with(session)
    refresh_session_repo_mock.create.assert_called_once()
    access_token_service_mock.issue.assert_called_once()


@pytest.mark.asyncio
async def test_execute_invalid_token(use_case, command, refresh_session_repo_mock):
    refresh_session_repo_mock.get_by_hash.return_value = None

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_execute_expired_session(use_case, command, refresh_session_repo_mock):
    session = Mock(spec=RefreshSessionDM, is_valid=Mock(return_value=False))
    refresh_session_repo_mock.get_by_hash.return_value = session

    with pytest.raises(AuthenticationFailed):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_execute_rate_limit_enforced(use_case, session, command, refresh_session_repo_mock, rate_limit_service_mock):
    refresh_session_repo_mock.get_by_hash.return_value = session

    await use_case.execute(command)

    rate_limit_service_mock.check.assert_any_call(
        'refresh:token:refresh_token_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v',
        use_case._token_rl_policy
    )
    rate_limit_service_mock.check.assert_any_call(
        'register:user_id:user-123',
        use_case._user_id_policy
    )