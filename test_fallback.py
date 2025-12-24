import os
from src.providers.openai_provider import OpenAIProvider
from src.providers.anthropic_provider import AnthropicProvider
from src.providers.ollama_provider import OllamaProvider
from src.providers.router import LLMRouter

# Setup providers (OpenAI → Anthropic → Ollama)
providers = [
    OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    ),
    AnthropicProvider(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-haiku-3-5-20241022"
    ),
]

# Add Ollama if available
try:
    providers.append(OllamaProvider(model="llama3.1:8b"))
except:
    print("Ollama not available - using cloud providers only")

# Create router
router = LLMRouter(providers=providers, max_retries=3)

# Test
print("\n" + "="*60)
print("Testing Multi-Vendor Fallback Chain")
print("="*60 + "\n")

response = router.generate("Write a haiku about AI")

print("\n" + "="*60)
print("RESULT")
print("="*60)
print(f"Response: {response.content}")
print(f"Provider: {response.provider}")
print(f"Model: {response.model}")
print(f"Cost: ${response.cost:.4f}")
print(f"Latency: {response.latency_ms:.0f}ms")
print(f"Tokens: {response.tokens_used}")

print("\n" + "="*60)
print("ROUTER STATISTICS")
print("="*60)
stats = router.get_stats()
for key, value in stats.items():
    print(f"{key}: {value}")
