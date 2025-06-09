import pytest
from csv_word_adapter import CSVWordAdapter
import os
import tempfile

@pytest.fixture
def sample_csv_file():
    """创建测试用CSV文件"""
    content = """tags,word,phonetics,meanings,examples,content
基础动词,understand,[ˌʌndərˈstænd],理解,I understand this math problem.
基础动词,discover,[dɪˈskʌvər],发现,Columbus discovered America.
"""
    with tempfile.NamedTemporaryFile(encoding='utf-8',mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
    yield f.name
    os.unlink(f.name)

@pytest.fixture
def empty_csv_file():
    """创建空CSV文件"""
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',  delete=False, suffix='.csv') as f:
        f.write("tags,word,phonetics,meanings,examples,content\n")
    yield f.name
    os.unlink(f.name)

def test_load_valid_csv(sample_csv_file):
    """测试正常CSV文件加载"""
    adapter = CSVWordAdapter(sample_csv_file)
    words = adapter.load_words()
    
    assert len(words) == 2
    assert words[0].word == 'understand'
    assert words[0].phonetics == '[ˌʌndərˈstænd]'
    assert words[1].meanings[0] == '发现'

def test_load_empty_csv(empty_csv_file):
    """测试空CSV文件"""
    adapter = CSVWordAdapter(empty_csv_file)
    words = adapter.load_words()
    
    assert len(words) == 0

def test_file_not_found():
    """测试文件不存在情况"""
    with pytest.raises(FileNotFoundError):
        adapter = CSVWordAdapter("nonexistent.csv")
        adapter.load_words()