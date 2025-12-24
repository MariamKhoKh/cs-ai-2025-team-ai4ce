import requests
import time
from .base_provider import LLMProvider, ProviderResponse, ProviderError

class OllamaProvider(LLMProvider):
    """Local Ollama provider - FREE fallback"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        super().__init__("", model, "Ollama")  # No API key needed
        self.base_url = base_url
    
    def generate(self, prompt: str, max_tokens: int = 500) -> ProviderResponse:
        start = time.time()
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens
                }
            },
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        latency = (time.time() - start) * 1000
        
        return ProviderResponse(
            content=data["response"],
            model=self.model,
            provider=self.name,
            tokens_used=0,  # Ollama doesn't provide token counts
            cost=0.0,  # Free!
            latency_ms=latency
        )
    
    def classify_error(self, error: Exception) -> ProviderError:
        error_msg = str(error).lower()
        
        if "connection" in error_msg:
            return ProviderError("api_error", "Ollama not running. Start with: ollama serve", provider=self.name)
        elif "timeout" in error_msg:
            return ProviderError("timeout", str(error), provider=self.name)
        else:
            return ProviderError("api_error", str(error), provider=self.name)
