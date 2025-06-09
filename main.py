# from llm_bridge import LLMBridge
# # Example usage
# llm = LLMBridge()

# # Use OpenAI
# # llm.set_active_config("openai")
# # response = llm.query("What is the capital of France?")
# # print(response)

# # Use local LM Studio
# llm.set_active_config("local-lmstudio")
# response = llm.query("What is the capital of France?")
# print(response)


from word_options_generator import WordOptionsGenerator

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


generate_options()