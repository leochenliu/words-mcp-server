from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Word:
    """单词数据模型"""
    word: str
    phonetics:Optional[str] = None  # 音标
    content: Optional[str] = None  # 词条内容
    meanings: Optional[List[str]] = None  # 含义列表
    examples: Optional[List[str]] = None  # 例句列表
    tags: Optional[List[str]] = None

    def __post_init__(self):
        # 初始化后自动验证
        if not self.word:
            raise ValueError("word 不能为空")
        # if not self.meanings or len(self.meanings) == 0:
        #     raise ValueError("meanings 不能为空")
        # if not self.tags:
        #     raise ValueError("tags 不能为空")
        
@dataclass
class Quiz:
    """测验数据模型"""
    id: int
    word: str
    meaning: str  # 仅使用一个含义进行测试
    options: List[str]
    correct_word: str    