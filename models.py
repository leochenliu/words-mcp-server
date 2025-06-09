from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Word:
    """单词数据模型"""
    word: str
    phonetics:Optional[str]
    content: Optional[str]
    meanings: List[str]
    examples: List[str]
    tags: Optional[List[str]] = None


@dataclass
class Quiz:
    """测验数据模型"""
    id: int
    word: str
    meaning: str  # 仅使用一个含义进行测试
    options: List[str]
    correct_word: str    