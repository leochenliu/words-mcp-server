

import json
import sys
import msvcrt
import os

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

def show_multiple_choice(word, options, correct_index):
    selected = 0
    while True:
        clear_screen()
        print(f'请选择{word}的正确含义：')
        for i, option in enumerate(options):
            prefix = '> ' if i == selected else '  '
            print(f'{prefix}{i + 1}. {option}')
        print('(使用↑↓方向键选择，Enter确认)')
        print('> 输入exit可随时退出')

        key = get_key()
        if key == 'UP' and selected > 0:
            selected -= 1
        elif key == 'DOWN' and selected < len(options) - 1:
            selected += 1
        elif key == 'ENTER':
            return selected == correct_index
        elif key == 'EXIT':
            sys.exit(0)

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
        
        # 显示选择题测试
        options = ['懒惰的', '勤奋的', '聪明的']
        correct = show_multiple_choice(word_data["word"], options, 1)
        print('回答' + ('正确！' if correct else '错误！'))
        print(f"\n正确答案是: {options[correct_index]}")
        print("按任意键继续...")
        msvcrt.getch()
        
        # 记录答题数据
        save_quiz_stats(
            total_time=45,  # 示例数据，实际使用时需要计算
            total_questions=20,
            correct_answers=15,
            wrong_answers=5,
            fastest_time=0.5,
            slowest_time=4.2,
            weak_topics={"商务英语": "3/5正确"}
        )
        
        return None

if __name__ == '__main__':
    words = load_words()
    for i, word in enumerate(words, 1):
        show_word(word, i, len(words))