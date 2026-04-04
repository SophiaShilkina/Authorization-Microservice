from .base import ConfigBase


class RateLimitRule(ConfigBase):
    attempts: int
    window_seconds: int


class RateLimitConfig(ConfigBase):
    login_email: RateLimitRule = RateLimitRule(attempts=5, window_seconds=15 * 60)
    login_ip: RateLimitRule = RateLimitRule(attempts=20, window_seconds=5 * 60)
    register_email: RateLimitRule = RateLimitRule(attempts=3, window_seconds=60 * 60)
    register_ip: RateLimitRule = RateLimitRule(attempts=10, window_seconds=60 * 60)
    refresh_token: RateLimitRule = RateLimitRule(attempts=30, window_seconds=5 * 60)
    refresh_token_user_id: RateLimitRule = RateLimitRule(attempts=10, window_seconds=60 * 60)
    logout_all: RateLimitRule = RateLimitRule(attempts=5, window_seconds=10 * 60)
