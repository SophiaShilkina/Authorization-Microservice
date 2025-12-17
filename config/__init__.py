from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

SETTINGS_PATH = PROJECT_ROOT / 'config' / 'settings'

__all__ = ['PROJECT_ROOT', 'SETTINGS_PATH']
