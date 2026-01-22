from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

import pytest
from unittest.mock import Mock, AsyncMock, MagicMock


@pytest.fixture
def user_repo_mock():
    mock = AsyncMock()
    mock.get_by_email.return_value = None
    mock.exists_by_email.return_value = False
    return mock


@asynccontextmanager
async def fake_transaction():
    yield


@pytest.fixture
def refresh_session_repo_mock():
    mock = AsyncMock()
    mock.get_by_hash.return_value = None
    mock.transaction = MagicMock(return_value=fake_transaction())
    return mock


@pytest.fixture
def password_hasher_mock():
    mock = Mock()
    mock.verify.return_value = True
    mock.dummy_verify.return_value = None
    mock.get_password_hash.return_value = 'password_hash_jro44223m3n32kn5n2ksdo4e234dsdom3k2kmdl3l43iwes9v'
    return mock


@pytest.fixture
def token_service_mock():
    mock = Mock()
    mock.hash_token.return_value = 'refresh_token_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v'
    mock.issue_refresh_token.return_value = (
        Mock(value='refresh_token_n5n2ksdo4edsdom3k2kmjro44223m3n3dl3l43iwes9v2k234'),
        Mock(value='refresh_token_hash_2kn5n2ksdo4e234dsdom3k2kmjro44223m3n3dl3l43iwes9v')
    )
    mock.issue_access_token.return_value = Mock(
        token='access_token_om3k2kmdsdjro4.4223m3n3dl3l43iw.n2ksdo4e234es9v2kn5',
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    payload_mock = Mock()
    payload_mock.user_id = "user-123"
    mock.verify_access_token.return_value = payload_mock
    return mock


@pytest.fixture
def email_service_mock():
    return AsyncMock()


@pytest.fixture
def rate_limit_service_mock():
    mock = AsyncMock()
    mock.check.return_value = None
    return mock


@pytest.fixture
def clock_mock():
    mock = Mock()
    mock.now.return_value = datetime.now(timezone.utc)
    return mock
