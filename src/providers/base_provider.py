from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderResponse:
    """Standard response format from any provider"""
    content: str
    model: str
    provider: str  # Added: track which provider responded
    tokens_used: int
    cost: float
    latency_ms: float

@dataclass
class ProviderError:
    """Standard error format"""
    error_type: str  # "rate_limit", "api_error", "timeout", "invalid_request"
    message: str
    retry_after: Optional[int] = None
    provider: str  # Added: track which provider failed

class LLMProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, api_key: str, model: str, name: str):
        self.api_key = api_key
        self.model = model
        self.name = name  # "OpenAI", "Anthropic", "Ollama"
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """Generate completion from this provider"""
        pass
    
    @abstractmethod
    def classify_error(self, error: Exception) -> ProviderError:
        """Classify error for fallback decisions"""
        pass
