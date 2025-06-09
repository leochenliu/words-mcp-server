import json
from llm_bridge import LLMBridge
from typing import List, Dict, Any
import os

class WordOptionsGenerator:
    def __init__(self):
        self.llm = LLMBridge()
        self.options_cache_file = "word_options_cache.json"
        self.options_cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load existing options cache from file"""
        if os.path.exists(self.options_cache_file):
            with open(self.options_cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save options cache to file"""
        with open(self.options_cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.options_cache, f, ensure_ascii=False, indent=2)

    def generate_distractors(self, word: str, correct_meaning: str) -> List[str]:
        """Generate distractor options for a given word"""
        
        # Check cache first
        if word in self.options_cache:
            return self.options_cache[word]['distractors']

        prompt = f"""
请为词语"{word}"生成3个干扰选项。要求：
1. 候选项与正确答案"{correct_meaning}"词性相同
2. 意思必须完全不同，不能有语义重叠
3. 如果是多义词，选取与正确答案最不相关的含义
4. 返回格式必须是JSON数组，包含3个字符串
5. 只返回JSON数组，不要其他解释

示例格式:
["选项1", "选项2", "选项3"]
"""

        response = self.llm.query(prompt)
        try:
            distractors = json.loads(response['content'])
            if not isinstance(distractors, list) or len(distractors) != 3:
                raise ValueError("Invalid response format")
            
            # Cache the results
            self.options_cache[word] = {
                'correct_meaning': correct_meaning,
                'distractors': distractors
            }
            self._save_cache()
            
            return distractors
        except Exception as e:
            print(f"Error generating distractors for {word}: {e}")
            return []

    def update_word_options(self, dictionary_file: str = 'dictionary.json'):
        """Update options for all words in dictionary"""
        with open(dictionary_file, 'r', encoding='utf-8') as f:
            words = json.load(f)

        for word_data in words:
            word = word_data['word']
            if "content" in word_data and "### 分析词义" in word_data['content']:
                correct_meaning = word_data['content'].split('### 分析词义')[1].split('###')[0].strip()
                print(f"Generating options for: {word}")
                self.generate_distractors(word, correct_meaning)

if __name__ == '__main__':
    generator = WordOptionsGenerator()
    generator.update_word_options()