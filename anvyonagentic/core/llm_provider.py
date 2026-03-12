"""LLM Provider abstraction and implementations"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class LLMResponse:
    """Response from LLM"""
    text: str
    tokens_used: int = 0
    model: str = ""


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Call the LLM with a prompt"""
        pass
    
    @abstractmethod
    def call_with_messages(self, messages: List[Dict[str, str]]) -> LLMResponse:
        """Call the LLM with a list of messages"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514"
    ):
        if not HAS_ANTHROPIC:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("AI_INTEGRATIONS_ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL") or os.environ.get("AI_INTEGRATIONS_ANTHROPIC_BASE_URL")
        self.model = model
        
        if not self.api_key:
            raise ValueError("Anthropic API key required")
        
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        
        self.client = anthropic.Anthropic(**client_kwargs)
    
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Call Claude with a prompt"""
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        
        response = self.client.messages.create(**kwargs)
        
        return LLMResponse(
            text=response.content[0].text,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            model=self.model
        )
    
    def call_with_messages(self, messages: List[Dict[str, str]]) -> LLMResponse:
        """Call Claude with messages"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=messages
        )
        
        return LLMResponse(
            text=response.content[0].text,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            model=self.model
        )
