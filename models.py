from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Word:
    """单词数据模型"""
    word: str
    content: Optional[str]
    meanings: List[str]
    examples: List[str]
    tags: Optional[List[str]] = None