import json
from typing import List, Optional
from word_source_adapter import WordSourceAdapter
from models import Word

class JSONWordAdapter(WordSourceAdapter):
    def load_words(self) -> List[Word]:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            words = []
            for item in data:
                # 解析content中的meanings和examples
                content = item['content']
                meanings = []
                examples = []
                
                if '### 分析词义' in content:
                    meanings_text = content.split('### 分析词义')[1].split('###')[0].strip()
                    meanings = [meanings_text]
                
                if '### 列举例句' in content:
                    examples_text = content.split('### 列举例句')[1].split('###')[0].strip()
                    examples = [ex.strip() for ex in examples_text.split('\n') if ex.strip()]
                
                word = Word(
                    word=item['word'],
                    content=content,
                    meanings=meanings,
                    examples=examples
                )
                words.append(word)
            return words
    
    def save_word(self, word: Word) -> bool:
        try:
            words = self.load_words()
            words = [w for w in words if w.word != word.word]  # Remove if exists
            words.append(word)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([{
                    'word': w.word,
                    'content': w.content
                } for w in words], f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving word to JSON: {e}")
            return False
    
    def get_word(self, word: str) -> Optional[Word]:
        words = self.load_words()
        for w in words:
            if w.word == word:
                return w
        return None