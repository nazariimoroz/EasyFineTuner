from py_singleton import singleton
import json
import pathlib
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QProcess
import sys

@singleton
class ACacheManager:
    def __init__(self):
        self.cache_dir = pathlib.Path.home() / '.cache' / 'easy_fine_tuner'
        self.datasets_cache = self.cache_dir / 'training_datasets.json'
        self.config_cache = self.cache_dir / 'config.json'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def load_training_datasets(self) -> dict:
        try:
            if self.datasets_cache.exists():
                with open(self.datasets_cache, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
        
    def save_training_datasets(self, datasets: dict):
        try:
            with open(self.datasets_cache, 'w') as f:
                json.dump(datasets, f)
        except Exception:
            pass
            
    def load_config(self) -> dict:
        try:
            if self.config_cache.exists():
                with open(self.config_cache, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
        
    def save_config(self, config: dict):
        try:
            with open(self.config_cache, 'w') as f:
                json.dump(config, f)

        except Exception:
            pass
            
    def get_api_key(self) -> str:
        config = self.load_config()
        return config.get('gemini_api_key', '')
        
    def set_api_key(self, api_key: str):
        config = self.load_config()
        config['gemini_api_key'] = api_key
        self.save_config(config)
        os.environ['GOOGLE_API_KEY'] = api_key

