from typing import Dict, Any, Optional, List
import os
import json
from openai import OpenAI
from dataclasses import dataclass

@dataclass
class LLMConfig:
    """Configuration for LLM service"""
    name: str
    api_key: str
    base_url: str
    model: str = "deepseek-chat"
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 1000

class LLMBridge:
    def __init__(self, config_path: str = "llm_config.json"):
        """
        Initialize LLM bridge with configurations
        
        Args:
            config_path (str): Path to configuration file
        """
        self.configs: Dict[str, LLMConfig] = {}
        self.active_config: Optional[str] = None
        self.load_configs(config_path)
        
    def load_configs(self, config_path: str) -> None:
        """Load configurations from JSON file"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                configs_dict = json.load(f)
                for name, cfg in configs_dict.items():
                    self.configs[name] = LLMConfig(**cfg)
                    if not self.active_config:
                        self.active_config = name

    def set_active_config(self, name: str) -> None:
        """Set active configuration by name"""
        if name not in self.configs:
            raise ValueError(f"Configuration '{name}' not found")
        self.active_config = name

    def get_client(self) -> OpenAI:
        """Get OpenAI client with current configuration"""
        if not self.active_config:
            raise ValueError("No active configuration set")
        
        config = self.configs[self.active_config]
        return OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )

    def query(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Send a query to the LLM service and get response
        
        Args:
            prompt (str): The input prompt to send to LLM
            **kwargs: Additional parameters for the query
            
        Returns:
            Dict[str, Any]: Response from LLM service
        """
        config = self.configs[self.active_config]
        client = self.get_client()
        
        messages = []
        if config.system_prompt:
            messages.append({"role": "system", "content": config.system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            temperature=kwargs.get('temperature', config.temperature),
            max_tokens=kwargs.get('max_tokens', config.max_tokens),
        )
        
        return self.process_response(response)

    def process_response(self, response: Any) -> Dict[str, Any]:
        """
        Process the raw response from LLM service
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Dict[str, Any]: Processed response
        """
        return {
            'content': response.choices[0].message.content,
            'finish_reason': response.choices[0].finish_reason,
            'model': response.model,
            'usage': response.usage.dict()
        }