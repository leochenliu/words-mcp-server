from abc import ABC, abstractmethod
from typing import List, Optional
from models import Word

class WordSourceAdapter(ABC):
    """词库数据源适配器基类"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    @abstractmethod
    def load_words(self) -> List[Word]:
        """加载所有单词"""
        pass
        
    @abstractmethod
    def save_word(self, word: Word) -> bool:
        """保存单个单词"""
        pass
        
    @abstractmethod
    def get_word(self, word: str) -> Optional[Word]:
        """获取指定单词"""
        pass