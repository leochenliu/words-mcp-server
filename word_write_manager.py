from typing import Dict
from word_source_adapter import WordSourceAdapter
from word_source_factory import WordSourceFactory
from models import Word
import logging

logger = logging.getLogger(__name__)
class WordWriteManager:
    def __init__(self):
        self.adapters = {}
    
    def get_adapter(self, path: str) -> WordSourceAdapter:
        if path not in self.adapters:
            self.adapters[path] = WordSourceFactory.create_adapter(path)
        return self.adapters[path]
    
    def save_word(self, path: str, word_data: Dict):
        """保存单词到指定词库"""
        if not path or not isinstance(path, str):
            logger.error("Invalid path provided for saving word")
            raise ValueError("Path must be a non-empty string")

        try:
            # 确保路径存在
            with open(path, 'a', encoding='utf-8') as file:
                adapter = self.get_adapter(path)
                return adapter.save_word(Word(**word_data))
        except FileNotFoundError as e:
            logger.error(f"Failed to save word to {path}: {e}")
            raise e            
        except Exception as e:
            logger.error(f"Failed to save word to {path}: {e}")
            raise e
        
