import csv
from typing import List, Optional
from word_source_adapter import WordSourceAdapter
from models import Word

class CSVWordAdapter(WordSourceAdapter):
    def load_words(self) -> List[Word]:
        words = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = Word(
                    word=row['word'],
                    phonetics=row['phonetics'],
                    content=row['content'],
                    meanings=row['meanings'].split('|'),
                    examples=row['examples'].split('|'),
                    tags=row.get('tags', '').split('|') if row.get('tags') else None
                )
                words.append(word)
        return words
    
    def save_word(self, word: Word) -> bool:
        try:
            # check input word, if invalid, raise ValueError
            words = self.load_words()
            words = [w for w in words if w.word != word.word]  # Remove if exists
            words.append(word)
            
            with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['word','phonetics', 'content', 'meanings', 'examples', 'tags'])
                writer.writeheader()
                for w in words:
                    writer.writerow({
                        'word': w.word,
                        'content': w.content,
                        'phonetics': w.phonetics,
                        'meanings': '|'.join(w.meanings) if w.meanings else '',
                        'examples': '|'.join(w.examples) if w.examples else '',
                        'tags': '|'.join(w.tags) if w.tags else ''
                    })
            return True
        except FileNotFoundError as fe:
            print(f"File not found: {fe}")
            return False
        except Exception as e:
            print(f"Error saving word to CSV: {e}")
            return False
    
    def get_word(self, word: str) -> Optional[Word]:
        words = self.load_words()
        for w in words:
            if w.word == word:
                return w
        return None