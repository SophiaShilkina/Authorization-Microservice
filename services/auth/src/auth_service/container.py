from auth_service.infrastructure.database.repositories import UserRepository, RefreshTokenRepository
from auth_service.infrastructure.security import PasswordHasher, JWTService, RandomTokenService
from auth_service.domain import PoliciesDomain
from auth_service.application import AuthService


class Container:
    def __init__(self):
        # Repo
        self.user_repo = UserRepository()
        self.refresh_token_repo = RefreshTokenRepository()

        # Infra
        self.password_hasher = PasswordHasher()
        self.jwt_service = JWTService()
        self.random_token_service = RandomTokenService()

        # Domain
        self.policies_domain = PoliciesDomain()

        # Application
        self.auth_service = AuthService(
            user_repo=self.user_repo,
            refresh_token_repo=self.refresh_token_repo,
            password_hasher=self.password_hasher,
            jwt_service=self.jwt_service,
            random_token_service=self.random_token_service,
            policies_domain=self.policies_domain,
        )


container = Container()
