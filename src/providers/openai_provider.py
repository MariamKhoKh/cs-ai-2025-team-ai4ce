
from openai import OpenAI
import time
from .base_provider import LLMProvider, ProviderResponse, ProviderError


class OpenAIProvider(LLMProvider):
    
    # Pricing per 1M tokens 
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """
        Generate completion from OpenAI.
        Returns standardized ProviderResponse with cost and latency.
        """
        start = time.time()
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        
        # Calculate latency
        latency = (time.time() - start) * 1000  # Convert to milliseconds
        
        # Calculate cost
        pricing = self.PRICING[self.model]
        input_cost = (response.usage.prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (response.usage.completion_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        return ProviderResponse(
            content=response.choices[0].message.content,
            model=self.model,
            tokens_used=response.usage.total_tokens,
            cost=total_cost,
            latency_ms=latency
        )
    
    def classify_error(self, error: Exception) -> ProviderError:
    
        error_msg = str(error).lower()
        
        if "rate_limit" in error_msg or "429" in error_msg:
            # Rate limited - wait 60 seconds or try different provider
            return ProviderError("rate_limit", str(error), retry_after=60)
        
        elif "timeout" in error_msg:
            # Timeout - try different provider
            return ProviderError("timeout", str(error))
        
        elif "invalid" in error_msg or "400" in error_msg:
            # Invalid request - don't retry, fail immediately
            return ProviderError("invalid_request", str(error))
        
        else:
            # Generic error - try different provider
            return ProviderError("api_error", str(error))
