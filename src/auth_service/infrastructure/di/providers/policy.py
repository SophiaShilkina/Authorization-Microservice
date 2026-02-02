from datetime import timedelta

from dishka import Provider, provide, Scope

from auth_service.application.security.policies import (
    TokenPolicy, LoginEmailRateLimit, LoginIPRateLimit, RegisterEmailRateLimit,
    RegisterIPRateLimit, RefreshTokenRateLimit, RefreshTokenUserIDRateLimit, LogoutAllRateLimit
)

from ...config import Config


class PolicyProvider(Provider):

    @provide(scope=Scope.APP)
    def token_policy(self, config: Config) -> TokenPolicy:
        return TokenPolicy(
            access_ttl=timedelta(minutes=config.access_token.ttl_minutes),
            refresh_ttl=timedelta(days=config.refresh_token.ttl_days),
        )

    @provide(scope=Scope.APP)
    def login_email_rate_limit(self, config: Config) -> LoginEmailRateLimit:
        rule = config.rate_limit.login_email
        return LoginEmailRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def login_ip_rate_limit(self, config: Config) -> LoginIPRateLimit:
        rule = config.rate_limit.login_ip
        return LoginIPRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def register_email_rate_limit(self, config: Config) -> RegisterEmailRateLimit:
        rule = config.rate_limit.register_email
        return RegisterEmailRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def register_ip_rate_limit(self, config: Config) -> RegisterIPRateLimit:
        rule = config.rate_limit.register_ip
        return RegisterIPRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def refresh_token_rate_limit(self, config: Config) -> RefreshTokenRateLimit:
        rule = config.rate_limit.refresh_token
        return RefreshTokenRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def refresh_token_user_id_rate_limit(self, config: Config) -> RefreshTokenUserIDRateLimit:
        rule = config.rate_limit.refresh_token_user_id
        return RefreshTokenUserIDRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )

    @provide(scope=Scope.APP)
    def logout_all_user_id_rate_limit(self, config: Config) -> LogoutAllRateLimit:
        rule = config.rate_limit.logout_all
        return LogoutAllRateLimit(
            attempts=rule.attempts,
            window=timedelta(seconds=rule.window_seconds),
        )
