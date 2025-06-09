import json
import random
import sys
import msvcrt
import os
import time
from word_options_generator import WordOptionsGenerator
from word_source_factory import WordSourceFactory

def load_words():
    """从配置的数据源加载词库"""
    try:
        with open('word_source_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        default_source = config['sources'][config['default_source']]
        adapter = WordSourceFactory.create_adapter(default_source['path'])
        return adapter.load_words()
    except Exception as e:
        print(f"Error loading words: {e}")
        return []

def show_word(word_data, index, total):
    print(f'> 单词: {word_data.word}')
    input('按回车继续...')
    
    # 显示词义分析
    if word_data.content:
        content = word_data.content
        # 提取并显示词义分析部分
        if "### 分析词义" in content:
            meaning = content.split("### 分析词义")[1].split("###")[0].strip()
            print(f'> 释义: {meaning}')
            input('按回车继续...')
        
        # 提取并显示例句
        if "### 列举例句" in content:
            examples = content.split("### 列举例句")[1].split("###")[0].strip()
            print(f'> 例句: {examples}')
            input('按回车继续...')
    else:
        # 直接显示meanings和examples
        if word_data.meanings:
            print(f'> 释义: {", ".join(word_data.meanings)}')
            input('按回车继续...')
        
        if word_data.examples:
            print(f'> 例句: \n{chr(10).join(word_data.examples)}')
            input('按回车继续...')

def generate_options(word_data):
    """生成选择题选项"""
    generator = WordOptionsGenerator()
    
    # 获取正确答案
    if word_data.content and "### 分析词义" in word_data.content:
        correct_meaning = word_data.content.split('### 分析词义')[1].split('###')[0].strip()
    else:
        correct_meaning = word_data.meanings[0] if word_data.meanings else ""
    
    # 获取干扰项
    distractors = generator.generate_distractors(word_data.word, correct_meaning)
    
    # 合并选项并打乱
    options = distractors + [correct_meaning]
    random.shuffle(options)
    
    return options, options.index(correct_meaning)

def show_multiple_choice(word_data):
    # ...existing code...
    print(f'请选择{word_data.word}的正确含义：')
    # ...rest of the existing code...

def create_quiz(word_data):
    # ...existing code...
    stats = {
        'word': word_data.word,
        'is_correct': is_correct,
        'answer_time': answer_time,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # ...rest of the existing code...

if __name__ == '__main__':
    words = load_words()  
    
    for i, word in enumerate(words, 1):
        #generate_options(word)
        show_word(word, i, len(words))    