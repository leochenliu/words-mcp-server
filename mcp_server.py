from fastmcp import FastMCP
from word_mcp_tool import WordTool
import asyncio

mcp = FastMCP("words_mcp")

if __name__ == "__main__":
    
    mcp.run(transport="sse", host="0.0.0.0", port=8000)