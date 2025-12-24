import time
from typing import List
from .base_provider import LLMProvider, ProviderResponse, ProviderError

class LLMRouter:
    """
    Robust multi-vendor fallback chain with retry logic.
    Try providers in order: OpenAI → Anthropic → Ollama
    """
    
    def __init__(self, providers: List[LLMProvider], max_retries: int = 3):
        self.providers = providers
        self.max_retries = max_retries
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "fallbacks_triggered": 0,
            "provider_usage": {p.name: 0 for p in providers}
        }
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """Try each provider in order until one succeeds"""
        self.stats["total_requests"] += 1
        
        last_error = None
        
        for provider_idx, provider in enumerate(self.providers):
            for retry in range(self.max_retries):
                try:
                    print(f"[Router] Trying {provider.name}/{provider.model} (attempt {retry + 1}/{self.max_retries})...")
                    
                    response = provider.generate(prompt, max_tokens)
                    
                    # Success!
                    self.stats["successful_requests"] += 1
                    self.stats["provider_usage"][provider.name] += 1
                    
                    if provider_idx > 0:
                        self.stats["fallbacks_triggered"] += 1
                        print(f"[Router] ✓ Fallback successful with {provider.name}")
                    else:
                        print(f"[Router] ✓ Success with {provider.name}")
                    
                    return response
                
                except Exception as e:
                    error = provider.classify_error(e)
                    last_error = error
                    
                    print(f"[Router] ✗ {provider.name} error: {error.error_type}")
                    
                    # If rate limited, wait and retry SAME provider
                    if error.error_type == "rate_limit" and retry < self.max_retries - 1:
                        wait_time = 2 ** retry  # Exponential backoff: 1s, 2s, 4s
                        print(f"[Router]   Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    
                    # If invalid request, don't retry - fail immediately
                    if error.error_type == "invalid_request":
                        raise Exception(f"Invalid request: {error.message}")
                    
                    # For other errors (timeout, api_error), try next provider
                    break
        
        # All providers failed
        raise Exception(f"All providers failed. Last error: {last_error.message if last_error else 'Unknown'}")
    
    def get_stats(self):
        """Return usage statistics"""
        return {
            **self.stats,
            "success_rate": self.stats["successful_requests"] / self.stats["total_requests"] if self.stats["total_requests"] > 0 else 0,
            "fallback_rate": self.stats["fallbacks_triggered"] / self.stats["total_requests"] if self.stats["total_requests"] > 0 else 0
        }
