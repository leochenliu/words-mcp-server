from word_source_factory import WordSourceFactory
import json

def load_word_source():
    with open('word_source_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    default_source = config['sources'][config['default_source']]
    adapter = WordSourceFactory.create_adapter(default_source['path'])
    return adapter

# 在需要加载词库的地方使用
word_source = load_word_source()
words = word_source.load_words()

for word in words:
    print(word.word)