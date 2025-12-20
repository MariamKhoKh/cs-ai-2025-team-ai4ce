

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProviderResponse:
    """Standard response format from any provider"""
    content: str           # The AI's response text
    model: str            # Which model was used (gpt-4o-mini, claude-haiku, ...)
    tokens_used: int      # Total tokens (input + output)
    cost: float           # Cost in USD
    latency_ms: float     # Response time in milliseconds


@dataclass
class ProviderError:
    """Standard error format for handling failures"""
    error_type: str       # "rate_limit", "api_error", "timeout", "invalid_request"
    message: str          # Error description
    retry_after: Optional[int] = None  # Seconds to wait before retrying (for rate limits)


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Forces each provider to implement generate() and classify_error()
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """
        Generate completion from this provider.
        Must be implemented by each provider (OpenAI, Anthropic, etc.)
        """
        pass
    
    @abstractmethod
    def classify_error(self, error: Exception) -> ProviderError:
        """
        Classify error for fallback decisions.
        Different providers have different error formats, so each must classify its own.
        """
        pass
