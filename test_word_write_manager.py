import pytest
from word_source_factory import WordSourceFactory
from word_write_manager import WordWriteManager
import os
import tempfile
import json
import csv
from typing import Dict
from models import Word

# test_csv_file_path = 'test_words.csv'

@pytest.fixture
def test_csv_file():
   
    """创建测试用CSV文件"""
    content = """tags,word,phonetics,meanings,examples,content
基础动词,understand,[ˌʌndərˈstænd],理解,I understand this math problem.,
"""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
        f.write(content)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def test_json_file():
    """创建测试用JSON文件"""
    content = {
        "understand": {
            "word": "understand",
            "meanings": ["理解"],
            "tags": ["基础动词"]
        }
    }
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.json') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def word_write_manager(test_csv_file):
    """创建WordWriteManager实例"""
    wm = WordWriteManager()

    wm.get_adapter(test_csv_file)
    return wm

def test_save_word_to_csv(word_write_manager, test_csv_file):
    """测试保存单词到CSV文件"""
    word_data = {
        "word": "apple",
        "meanings": ["苹果"],
        "tags": ["水果"],
        "phonetics": "[ˈæpl]",
        "examples": ["I eat an apple."],
        "content": ""
    }
    
    # 保存单词
    word_write_manager.save_word(test_csv_file, Word(**word_data))
 

    # 验证保存结果
    with open(test_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 2  # 包括原有的一行和新增的一行
        new_word = Word(**rows[1])
        assert new_word.word == 'apple'
        assert new_word.meanings == '苹果'
        assert new_word.tags == '水果'

# def test_save_word_to_json(word_write_manager, test_json_file):
#     """测试保存单词到JSON文件"""
#     word_data = {
#         "word": "apple",
#         "meanings": ["苹果"],
#         "tags": ["水果"]
#     }
    
#     # 保存单词
#     word_write_manager.save_word(test_json_file, word_data)
    
#     # 验证保存结果
#     with open(test_json_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         assert 'apple' in data
#         saved_word = data['apple']
#         assert saved_word['meanings'] == ['苹果']
#         assert saved_word['tags'] == ['水果']

def test_save_word_invalid_path(word_write_manager):
    """测试保存到无效路径"""
    word_data = {
        "word": "apple",
        "meanings": ["苹果"],
        "tags": ["水果"]
    }
    
    with pytest.raises(FileNotFoundError):
        word_write_manager.save_word("/invalid/path/words.csv", Word(**word_data))

def test_save_word_invalid_format(word_write_manager, test_csv_file):
    """测试保存格式无效的数据"""
    invalid_data = {
        "word": None,  # 无效的单词
        "meanings": [],  # 空的含义列表
        "tags": None  # 无效的标签
    }
    
    with pytest.raises(ValueError):
        word_write_manager.save_word(test_csv_file, Word(**invalid_data))

def test_update_existing_word(word_write_manager, test_csv_file):
    """测试更新已存在的单词"""
    # 更新 understand 的含义
    update_data = {
        "word": "understand",
        "meanings": ["理解", "懂得"],
       "tags": ["基础动词", "重要词汇"]
    }
    
    word_write_manager.save_word(test_csv_file, Word(**update_data))
    
    # 验证更新结果
    with open(test_csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1  

        updated_word = rows[0]
        #assert len(updated_word['meanings']) == 2
        assert '懂得' in updated_word['meanings']
        assert '重要词汇' in updated_word['tags']

