import asyncio
from typing import Dict, List
from llm_bridge import LLMBridge
import logging
from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.resources import ResourceManager,Resource
from word_write_manager import WordWriteManager
import logging.config

# 加载配置文件
logging.config.fileConfig('logging.conf')

logger = logging.getLogger(__name__)
# 设置日志记录器的级别为 DEBUG（关键步骤）
logger.setLevel(logging.DEBUG)

# 创建FastMCP实例
mcp = FastMCP("words_mcp", transport="sse")
logger.debug("FastMCP instance created")


class WordTool():
    """单词管理工具"""
    
    def __init__(self):
        # super().__init__(
        #     name="word_tool",
        #     description="管理词库中的单词资源",
        #     version="1.0"
        # )
        self.save_file_path = 'new_words.csv'
        self.llm = LLMBridge()
        self.word_write_manager = WordWriteManager()
        self.word_write_manager.get_adapter(self.save_file_path)
        # 初始化资源管理器，设置重复处理策略为替换
        self.resource_manager = ResourceManager(duplicate_behavior="replace")

    
    async def add_words(self, words: List[str]) -> Dict:
        """批量添加多个单词到词库"""
        try:
            results = []
            for word in words:
                # 检查单词是否已存在
                if self.resource_manager.has_resource(f"word://{word}"):
                    logger.info(f"Word {word} already exists, will update")
                
                # 获取单词释义
                prompt = f"Provide Chinese meanings for the English word '{word}' in JSON array format"
                response = await self.llm.query(prompt)
                meanings = response.get('content', [])

                # 创建单词资源
                word_resource = Resource(
                    uri=f"word://{word}",
                    name=word,
                    description=f"English word: {word}",
                    data={
                        "word": word,
                        "meanings": meanings
                    },
                    tags={"vocabulary", "english"}
                )
                
                # 添加到资源管理器
                try:
                    self.resource_manager.add_resource(word_resource)
                    results.append({
                        "word": word,
                        "meanings": meanings,
                        "status": "success"
                    })
                    logger.info(f"Added word resource: {word}")
                except Exception as e:
                    logger.error(f"Failed to add word resource {word}: {e}")
                    results.append({
                        "word": word,
                        "status": "error",
                        "error": str(e)
                    })
            
            return {
                "status": "success",
                "message": f"Processed {len(words)} words",
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Batch word addition failed: {e}")
            return {
                "status": "error",
                "message": f"Failed to process words: {str(e)}"
            }
        
    
    async def add_word(self, word: str) -> Dict:
        """添加单个单词（兼容接口）"""
        logger.debug(f"Adding single word: {word}")
        self.word_write_manager.save_word(self.save_file_path, {"word":word})
        return {
            "status": "success",
            "message": f"Word added successfully: {word}"
        }
        # return await self.add_words([word])
    async def add_words(self, words: List[str]) -> Dict:
        """批量添加多个单词到词库"""
        logger.debug(f"Adding words: {words}")
        for word in words:
            # 检查单词是否已存在
            self.word_write_manager.save_word(self.save_file_path, {"word":word})

        return {
            "status": "success",
            "message": f"Words added successfully: {', '.join(words)}"
        }

    def get_word(self, word: str) -> Dict:
        """获取单词信息"""
        try:
            resource = self.resource_manager.get_resource(f"word://{word}")
            return {
                "status": "success",
                "word": resource.data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Word not found: {str(e)}"
            }

@mcp.tool("add_word")
async def add_word(word: str) -> Dict:
    """添加单个单词"""
    word_tool = WordTool()
    logger.debug(f"Adding word: {word}")
    return await word_tool.add_word(word)

@mcp.tool("add_words_list")
async def add_words(word_list: List[str]) -> Dict:
    """批量添加多个单词到词库"""
    word_tool = WordTool()
    logger.debug(f"Adding words: {word_list}")
    return await word_tool.add_words(word_list)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
    logger.debug("MCP server started on port 8000") 
