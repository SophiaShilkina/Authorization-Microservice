from .dto import LoginCommand, LoginResult
from .ports import


class AuthService:
    def __init__(self,
                 user_repo: UserRepositoryProtocol,
                 refresh_token_repo,
                 password_hasher,
                 jwt_service,
                 random_token_service,
                 policies_domain,
                 ):
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service
        self.random_token_service = random_token_service
        self.policies_domain = policies_domain


    async def login(self, cmd: LoginCommand) -> LoginResult:
        user = await self.user_repo.get_all_by_email(cmd.email)

        self.policies_domain.

        access = self.token_issuer.issue_access(user)
        refresh = await self.token_issuer.issue_refresh(user, cmd.context)

        return LoginResult(access, refresh)
