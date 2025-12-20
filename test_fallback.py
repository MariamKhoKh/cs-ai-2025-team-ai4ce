import os
from dotenv import load_dotenv
from src.providers.openai_provider import OpenAIProvider
from src.providers.anthropic_provider import AnthropicProvider
from src.providers.router import SimpleRouter

# Load environment variables
load_dotenv()


def test_fallback():
    """Test the fallback chain with both providers"""
    
    print("="*60)
    print("TESTING MULTI-VENDOR FALLBACK SYSTEM")
    print("="*60)
    print()
    
    # Setup OpenAI provider (primary)
    print("📦 Setting up OpenAI (primary provider)...")
    openai = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )
    print(f"   ✓ Model: {openai.model}")
    print()
    
    # Setup Anthropic provider (backup)
    print("📦 Setting up Anthropic (backup provider)...")
    anthropic = AnthropicProvider(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-haiku-3-5-20241022"
    )
    print(f"   ✓ Model: {anthropic.model}")
    print()
    
    # Create router with fallback chain
    print("🔗 Creating fallback chain: OpenAI → Anthropic")
    router = SimpleRouter(providers=[openai, anthropic])
    print("   ✓ Router ready")
    print()
    
    # Test with a simple prompt
    print("="*60)
    print("SENDING TEST PROMPT")
    print("="*60)
    print()
    prompt = "Write a haiku about artificial intelligence"
    print(f"Prompt: {prompt}")
    print()
    
    try:
        # Generate response (will use whichever provider works)
        response = router.generate(prompt, max_tokens=100)
        
        # Display results
        print()
        print("="*60)
        print("✅ SUCCESS - RESPONSE RECEIVED")
        print("="*60)
        print()
        print(f"📝 Response:")
        print(f"   {response.content}")
        print()
        print(f"📊 Metadata:")
        print(f"   Model Used:    {response.model}")
        print(f"   Tokens Used:   {response.tokens_used}")
        print(f"   Cost:          ${response.cost:.6f}")
        print(f"   Latency:       {response.latency_ms:.0f}ms")
        print()
        print("="*60)
        
    except Exception as e:
        print()
        print("="*60)
        print("❌ ERROR - ALL PROVIDERS FAILED")
        print("="*60)
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check that both API keys are set in .env")
        print("2. Verify you have API credits available")
        print("3. Check internet connection")


def test_cost_comparison():
    """Compare costs between providers"""
    
    print("\n")
    print("="*60)
    print("COST COMPARISON")
    print("="*60)
    print()
    
    prompt = "Explain quantum computing in one paragraph"
    
    # OpenAI
    openai = OpenAIProvider(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini"
    )
    
    try:
        openai_response = openai.generate(prompt, max_tokens=150)
        print(f"OpenAI (gpt-4o-mini):")
        print(f"   Cost: ${openai_response.cost:.6f}")
        print(f"   Tokens: {openai_response.tokens_used}")
        print(f"   Latency: {openai_response.latency_ms:.0f}ms")
        print()
    except Exception as e:
        print(f"OpenAI failed: {e}")
        print()
    
    # Anthropic
    anthropic = AnthropicProvider(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-haiku-3-5-20241022"
    )
    
    try:
        anthropic_response = anthropic.generate(prompt, max_tokens=150)
        print(f"Anthropic (claude-haiku):")
        print(f"   Cost: ${anthropic_response.cost:.6f}")
        print(f"   Tokens: {anthropic_response.tokens_used}")
        print(f"   Latency: {anthropic_response.latency_ms:.0f}ms")
        print()
    except Exception as e:
        print(f"Anthropic failed: {e}")
        print()


if __name__ == "__main__":
    # Run basic fallback test
    test_fallback()
    
    # Optional: Compare costs
    # Uncomment to see cost comparison
    # test_cost_comparison()
