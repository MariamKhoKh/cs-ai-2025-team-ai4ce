

import time
from typing import List
from .base_provider import LLMProvider, ProviderResponse, ProviderError


class SimpleRouter:
    
    def __init__(self, providers: List[LLMProvider], max_retries: int = 3):

        self.providers = providers
        self.max_retries = max_retries
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:

        
        # Try each provider in order
        for provider in self.providers:
            
            # Retry same provider up to max_retries times
            for retry in range(self.max_retries):
                try:
                    print(f"🔄 Trying {provider.model} (attempt {retry + 1}/{self.max_retries})...")
                    
                    # Call the provider
                    response = provider.generate(prompt, max_tokens)
                    
                    print(f"✅ Success with {provider.model}")
                    return response
                
                except Exception as e:
                    # Classify the error to decide what to do
                    error = provider.classify_error(e)
                    print(f"❌ Error: {error.error_type} - {error.message[:100]}")
                    
                    # CASE 1: Rate Limited
                    # Wait and retry same provider (exponential backoff)
                    if error.error_type == "rate_limit" and retry < self.max_retries - 1:
                        wait_time = 2 ** retry  # 1s, 2s, 4s
                        print(f"⏳ Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue  # Try same provider again
                    
                    # CASE 2: Invalid Request
                    # Don't retry - the prompt itself is bad
                    if error.error_type == "invalid_request":
                        print(f"🚫 Invalid request. Not retrying.")
                        raise Exception(f"Invalid request: {error.message}")
                    
                    # CASE 3: Other Errors (timeout, api_error)
                    # Move to next provider
                    print(f"⏭️  Moving to next provider...")
                    break  # Exit retry loop, try next provider
        
        # If we get here, all providers failed
        raise Exception("❌ All providers failed. Unable to generate response.")


class AdvancedRouter(SimpleRouter):

    
    def __init__(self, providers: List[LLMProvider], max_retries: int = 3):
        super().__init__(providers, max_retries)
        self.usage_stats = {provider.model: {"calls": 0, "total_cost": 0.0} for provider in providers}
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        """Generate with usage tracking"""
        response = super().generate(prompt, max_tokens)
        
        # Track usage
        self.usage_stats[response.model]["calls"] += 1
        self.usage_stats[response.model]["total_cost"] += response.cost
        
        return response
    
    def get_usage_stats(self):
       
        return self.usage_stats
