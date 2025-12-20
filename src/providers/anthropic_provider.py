
from anthropic import Anthropic
import time
from .base_provider import LLMProvider, ProviderResponse, ProviderError


class AnthropicProvider(LLMProvider):
    """Anthropic (Claude) implementation with Sonnet and Haiku support"""
    
    # Pricing per 1M tokens
    PRICING = {
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-haiku-3-5-20241022": {"input": 0.80, "output": 4.00},
    }
    
    def __init__(self, api_key: str, model: str = "claude-haiku-3-5-20241022"):
        super().__init__(api_key, model)
        # Initialize Anthropic client
        self.client = Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """
        Generate completion from Anthropic Claude.
        Returns standardized ProviderResponse with cost and latency.
        """
        start = time.time()
        
        # Call Anthropic API
        # Note: Anthropic uses messages.create instead of chat.completions.create
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Calculate latency
        latency = (time.time() - start) * 1000  # Convert to milliseconds
        
        # Calculate cost (same formula as OpenAI, different pricing)
        pricing = self.PRICING[self.model]
        input_cost = (response.usage.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (response.usage.output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        return ProviderResponse(
            content=response.content[0].text,  # Note: Anthropic uses content[0].text
            model=self.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            cost=total_cost,
            latency_ms=latency
        )
    
    def classify_error(self, error: Exception) -> ProviderError:
        """
        Classify Anthropic errors for fallback decisions.
        Same logic as OpenAI since error types are similar.
        """
        error_msg = str(error).lower()
        
        if "rate_limit" in error_msg or "429" in error_msg:
            # Rate limited - wait 60 seconds or try different provider
            return ProviderError("rate_limit", str(error), retry_after=60)
        
        elif "timeout" in error_msg:
            # Timeout - try different provider
            return ProviderError("timeout", str(error))
        
        elif "invalid" in error_msg:
            # Invalid request - don't retry, fail immediately
            return ProviderError("invalid_request", str(error))
        
        else:
            # Generic error - try different provider
            return ProviderError("api_error", str(error))
