import os
from csv_word_adapter import CSVWordAdapter
from json_word_adapter import JSONWordAdapter
from word_source_adapter import WordSourceAdapter

class WordSourceFactory:
    @staticmethod
    def create_adapter(file_path: str) -> WordSourceAdapter:
        """根据文件扩展名创建对应的适配器"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return CSVWordAdapter(file_path)
        elif ext == '.json':
            return JSONWordAdapter(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")