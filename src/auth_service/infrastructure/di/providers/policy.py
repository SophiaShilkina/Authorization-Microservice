from datetime import timedelta

from dishka import Provider, provide, Scope

from auth_service.application.security.policies import TokenPolicy, RateLimitPolicy


class PolicyProvider(Provider):

    @provide(scope=Scope.APP)
    def token_policy(self) -> TokenPolicy:
        return TokenPolicy(
            access_ttl=timedelta(minutes=15),
            refresh_ttl=timedelta(days=7),
        )

    @provide(scope=Scope.APP)
    def login_email_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )

    @provide(scope=Scope.APP)
    def login_ip_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )

    @provide(scope=Scope.APP)
    def register_email_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )

    @provide(scope=Scope.APP)
    def register_ip_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )

    @provide(scope=Scope.APP)
    def refresh_token_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )

    @provide(scope=Scope.APP)
    def logout_all_user_id_rate_limit(self) -> RateLimitPolicy:
        return RateLimitPolicy(
            attempts=5,
            window=timedelta(minutes=5),
        )
