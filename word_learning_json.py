

import json
import random
import sys
import msvcrt
import os
from word_options_generator import WordOptionsGenerator

def load_words():
    with open('dictionary.json', encoding='utf-8') as f:
        return json.load(f)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    first_char = msvcrt.getch()
    if first_char == b'\xe0':  # 特殊键的前缀
        second_char = msvcrt.getch()
        if second_char == b'H':  # 上箭头
            return 'UP'
        elif second_char == b'P':  # 下箭头
            return 'DOWN'
    elif first_char == b'\r':  # 回车键
        return 'ENTER'
    elif first_char == b'\x1b':  # ESC键
        return 'EXIT'
    return None

import json
import os
import time

def save_quiz_stats(total_time, total_questions, correct_answers, wrong_answers, fastest_time, slowest_time, weak_topics):
    stats = {
        "total_time": total_time,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "accuracy": round(correct_answers/total_questions*100, 2),
        "average_time": round(total_time/total_questions, 2),
        "fastest_time": fastest_time,
        "slowest_time": slowest_time,
        "weak_topics": weak_topics,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not os.path.exists("quiz_stats.json"):
        with open("quiz_stats.json", "w", encoding="utf-8") as f:
            json.dump([stats], f, ensure_ascii=False, indent=2)
    else:
        with open("quiz_stats.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(stats)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)

def generate_options(word_data):
    """生成选择题选项"""
    # 从词库中获取正确答案
    correct_meaning = word_data['content'].split('### 分析词义')[1].split('###')[0].strip()
    
    # 生成3个干扰项
    with open('dictionary.json', encoding='utf-8') as f:
        all_words = json.load(f)
        other_meanings = [w['content'].split('### 分析词义')[1].split('###')[0].strip() 
                         for w in all_words if w['word'] != word_data['word']]
    
    # 随机选择3个干扰项
    import random
    options = random.sample(other_meanings, 3)
    options.append(correct_meaning)
    random.shuffle(options)
    
    return options, options.index(correct_meaning)

def show_multiple_choice(word_data):
    """显示选择题测试界面"""
    options, correct_index = generate_options(word_data)
    selected = 0
    start_time = time.time()
    
    while True:
        clear_screen()
        print(f'请选择{word_data["word"]}的正确含义：')
        for i, option in enumerate(options):
            prefix = '> ' if i == selected else '  '
            print(f'{prefix}{i + 1}. {option}')
        print('(使用↑↓方向键选择，Enter确认)')
        print('> 输入ESC可随时退出')

        key = get_key()
        if key == 'UP' and selected > 0:
            selected -= 1
        elif key == 'DOWN' and selected < len(options) - 1:
            selected += 1
        elif key == 'ENTER':
            end_time = time.time()
            answer_time = end_time - start_time
            is_correct = selected == correct_index
            
            clear_screen()
            print('回答' + ('正确！' if is_correct else '错误！'))
            print(f"\n正确答案是: {options[correct_index]}")
            print(f"用时: {answer_time:.1f}秒")
            print("按任意键继续...")
            msvcrt.getch()
            
            return is_correct, answer_time
            
        elif key == 'EXIT':
            sys.exit(0)

def create_quiz():
        # 显示选择题测试
        is_correct, answer_time = show_multiple_choice(word_data)
        
        # 更新统计信息
        stats = {
            'word': word_data['word'],
            'is_correct': is_correct,
            'answer_time': answer_time,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 保存单次测试结果
        if not os.path.exists("quiz_results.json"):
            with open("quiz_results.json", "w", encoding="utf-8") as f:
                json.dump([stats], f, ensure_ascii=False, indent=2)
        else:
            with open("quiz_results.json", "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(stats)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)


def show_word(word_data, index, total):
    print(f'> 单词: {word_data["word"]}')
    input('按回车继续...')
    
    # 显示词义分析
    if "content" in word_data:
        content = word_data["content"]
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
        
       
        return None

def generate_options(word_data):
    """生成选择题选项"""
    generator = WordOptionsGenerator()
    correct_meaning = word_data['content'].split('### 分析词义')[1].split('###')[0].strip()
    
    # 获取干扰项
    distractors = generator.generate_distractors(word_data['word'], correct_meaning)
    
    # 合并选项并打乱
    options = distractors + [correct_meaning]
    random.shuffle(options)
    
    return options, options.index(correct_meaning)

if __name__ == '__main__':
    words = load_words()
    
    for i, word in enumerate(words, 1):
        #generate_options(word)
        show_word(word, i, len(words))