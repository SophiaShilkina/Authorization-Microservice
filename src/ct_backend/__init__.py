from pathlib import Path
from .core.config import Config

PROJECT_ROOT = Path(__file__).parent.parent
SRC_ROOT = Path(__file__).parent
SETTINGS_PATH = PROJECT_ROOT / 'settings'

config = Config.load()

__all__ = ['PROJECT_ROOT', 'SRC_ROOT', 'SETTINGS_PATH', 'config']
