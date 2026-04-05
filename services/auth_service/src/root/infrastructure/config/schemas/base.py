from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

INFRA_DIR = Path(__file__).resolve().parent.parent.parent.parent
SETTINGS_PATH = INFRA_DIR / 'secrets'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_file=(SETTINGS_PATH / '.env.template', SETTINGS_PATH / '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )


class AppConfig(ConfigBase):
    base_dir: Path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
    timezone: str = 'UTC'
