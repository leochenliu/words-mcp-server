import json
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict
from typing import List,Dict
# from pydantic import BaseModel

# 创建FastMCP实例
mcp = FastMCP("Vocabulary Stats", transport="sse")

# 词库统计资源
# Define a sample resource
class VocabularyResource(BaseModel):
    name: str = "vocabulary"
    description: str = "Manages vocabulary data"
    words: List[Dict[str, str]] = []
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_words(self) -> list[str]:
        # This would typically load from a database or file
        with open('dictionary.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        return sorted([item["word"] for item in dictionary if "word" in item])

    def get_word_count(self) -> int:
        with open('dictionary.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        return len(dictionary)

@mcp.resource("vocabulary://stats")
def get_vocabulary_stats() -> dict:
    """获取词库统计信息"""
    resource = VocabularyResource()
    return {
        'word_count': resource.get_word_count(),
        'word_list': resource.get_words()
    }

# 词库统计工具
@mcp.tool("get_vocabulary_stats_tool")
def get_vocabulary_stats_tool(resource:VocabularyResource)->dict:
    """获取词库统计信息的工具"""
    return {
        "word_count": resource.get_word_count(),
        "word_list": resource.get_words()
    }

# 词库状态提示
@mcp.prompt()
def vocabulary_status_prompt() -> str:
    """词库状态提示模板"""
    stats = get_vocabulary_stats()
    return f"当前词库包含 {stats['word_count']} 个单词"


class VocabularyStats(BaseModel):

    dictionary_path: str
    vocabulary_resource: VocabularyResource
    server: FastMCP

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, dictionary_path='dictionary.json'):
        
        super().__init__(
            dictionary_path=dictionary_path,
            vocabulary_resource=VocabularyResource(),
            server=FastMCP(
                'mcp dict',
                transport="sse",
                resources=[VocabularyResource()],
                tools=[get_vocabulary_stats_tool]
            )
        )

    def load_dictionary(self):
        with open(self.dictionary_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def get_stats(self):
        dictionary = self.load_dictionary()
        word_count = len(dictionary)
        word_list = sorted(list(dictionary.keys()))
        return {
            'word_count': word_count,
            'word_list': word_list
        }

if __name__ == '__main__':
    stats = VocabularyStats()
    print("Starting MCP server with vocabulary stats resource and tool...")
    # The get_stats method is now part of the resource/tool, 
    # so direct printing like before is not the primary way to interact.
    # The server will expose these via its API.
    stats.server.run(transport="sse", host="0.0.0.0", port=8000)