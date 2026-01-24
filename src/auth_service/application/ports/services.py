from typing import Protocol
from datetime import datetime


class IEmailService(Protocol):
    """Interface (port) for email service"""

    async def send_verification_email(self, email: str, username: str) -> bool: ...


class IClock(Protocol):
    """Interface (port) for clock service"""

    def now(self) -> datetime: ...
