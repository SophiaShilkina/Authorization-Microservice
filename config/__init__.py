from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

SETTINGS_PATH = PROJECT_ROOT / 'config' / 'settings'

from .main import Config

config = Config.load()

__all__ = ['PROJECT_ROOT', 'SETTINGS_PATH', 'config']
