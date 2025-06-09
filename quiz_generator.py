import os
import csv
import json
import random
from typing import List, Dict
from models import Word, Quiz
from logger_config import logger
from llm_bridge import LLMBridge

class QuizGenerator:
    def __init__(self):
        self.llm = LLMBridge()
        self.quiz_data_file = "quiz_data.json"
        self.quiz_data = self._load_quiz_data()
        self.current_quiz_id = len(self.quiz_data.get('quizzes', []))

    def read_words(self, csv_path: str) -> List[Word]:
        """Read words from CSV file and convert to Word objects"""
        words = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert meanings string to list
                meanings = [m.strip() for m in row['meanings'].split(';') if m.strip()]
                examples = [e.strip() for e in row['examples'].split(';') if e.strip()]
                tags = [row['tags']] if row['tags'] else []
                
                word = Word(
                    word=row['word'],
                    phonetics=row['phonetics'],
                    meanings=meanings,
                    examples=examples,
                    tags=tags,
                    content=row.get('content')
                )
                words.append(word)
        return words

    def selected_meaning(self, word: Word) -> str:
        """Randomly select one meaning for the quiz"""
        return random.choice(word.meanings)
    
    def generate_quiz(self, word: Word, selected_meaning: str,
                      all_words: List[Word]) -> Quiz:
        """Generate a quiz from a word"""

        # Generate options (other words as distractors)
        options = all_words + [word.word]
        random.shuffle(options)

        # Create quiz object
        self.current_quiz_id += 1
        quiz = Quiz(
            id=self.current_quiz_id,
            word=word.word,
            meaning=selected_meaning,
            options=options,
            correct_word=word.word
        )

        # Save to quiz data
        if 'quizzes' not in self.quiz_data:
            self.quiz_data['quizzes'] = []
        
        self.quiz_data['quizzes'].append({
            'id': quiz.id,
            'word': quiz.word,
            'meaning': quiz.meaning,
            'options': quiz.options,
            'correct_word': quiz.correct_word
        })
        
        self._save_quiz_data()
        logger.info(f"Created and saved quiz {quiz.id} for word: {quiz.word}")
        
        return quiz

    def _load_quiz_data(self) -> Dict:
        """Load existing quiz data from file"""
        if os.path.exists(self.quiz_data_file):
            with open(self.quiz_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'quizzes': []}

    def _save_quiz_data(self):
        """Save quiz data to file"""
        with open(self.quiz_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.quiz_data, f, ensure_ascii=False, indent=2)

    def generate_options(self, word: str, meaning: str, num_options: int = 4) -> List[str]:
        """Generate multiple choice options using LLM"""
        prompt = f"""
Given the word "{word}" with the correct meaning "{meaning}", generate {num_options-1} plausible distractor words that belong to the different category and are commonly confused with "{word}". The distractor words must not share the meaning "{meaning}". Return only the distractor words, separated by '|'.
.
        """
        logger.debug(f"Generating options for word: {word} with prompt: {prompt}")

        response = self.llm.query(prompt)
        logger.debug(f"LLM response: {response}")

        try:
            content = response['content']
            if isinstance(content, str):
                options = content.split('|')
                options = [opt.strip() for opt in options]
                random.shuffle(options)

                logger.info(f"Saved quiz data for word: {word}")
                return options
        except Exception as e:
            logger.error(f"Error generating options for {word}: {e}")
            return []


# Example usage
if __name__ == "__main__":
    quiz_gen = QuizGenerator()
    
    # Read words from CSV
    words = quiz_gen.read_words('words.csv')
    
    # Generate a quiz question for the first word
    for word in words:
        selected_meaning = quiz_gen.selected_meaning(word)
        all_words = quiz_gen.generate_options(word,selected_meaning)
        quiz = quiz_gen.generate_quiz(word,selected_meaning, all_words)
        print(f"Word: {quiz.word}")
        print("Options:")
        for i, option in enumerate(quiz.options, 1):
            print(f"{i}. {option}")
        print(f"\nCorrect answer: {quiz.correct_word}")                