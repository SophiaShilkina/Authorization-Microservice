from auth_service.application.ports import IEmailService


class FakeEmailService(IEmailService):
    async def send_verification_email(self, email: str, username: str) -> bool:
        return True
