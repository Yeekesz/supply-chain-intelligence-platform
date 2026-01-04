import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration manager"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self._config = None
    
    @property
    def config(self):
        if self._config is None:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)
        return self._config
    
    def get(self, key: str, default=None):
        """Get config value by key"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    @staticmethod
    def get_env(key: str, default: str = None):
        """Get environment variable"""
        return os.getenv(key, default)

config = Config()