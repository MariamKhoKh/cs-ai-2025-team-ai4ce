import os
import time
import hashlib
from typing import Dict, Any
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool, content_types
from dotenv import load_dotenv
from src.backend.functions.tools import (
    analyze_code_submission,
    get_recommended_problem,
    track_user_progress
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ==================== OPTIMIZATION 1: RESPONSE CACHE ====================

class ResponseCache:
    """Simple TTL cache for identical requests"""
    
    def __init__(self, ttl_seconds=300):  # 5 min default
        self.cache = {}
        self.ttl = ttl_seconds
    
    def _make_key(self, function_name: str, args: Dict) -> str:
        """Create cache key from function + args"""
        key_str = f"{function_name}:{str(sorted(args.items()))}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, function_name: str, args: Dict) -> Any:
        """Get cached result if fresh"""
        key = self._make_key(function_name, args)
        
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                print(f"🎯 Cache HIT: {function_name}")
                return result
            else:
                del self.cache[key]  # Expired
        
        return None
    
    def set(self, function_name: str, args: Dict, result: Any):
        """Cache result"""
        key = self._make_key(function_name, args)
        self.cache[key] = (result, time.time())


# ==================== OPTIMIZATION 2: TOKEN REDUCTION ====================

# BEFORE: Verbose system prompt (500 tokens)
# AFTER: Concise prompt (200 tokens) - 60% reduction

OPTIMIZED_SYSTEM_PROMPT = """You help users prepare for coding interviews.

Tools:
- analyze_code_submission: Run tests, detect patterns, give feedback
- get_recommended_problem: Suggest next problem based on weaknesses  
- track_user_progress: Update mastery scores after submission

Be concise and actionable."""


# ==================== OPTIMIZATION 3: DUAL MODEL ROUTING ====================

def choose_model(function_name: str) -> str:
    """Route to appropriate model based on task complexity"""
    
    # Simple read operations → use cheaper model
    if function_name == "get_recommended_problem":
        return "models/gemini-1.5-flash"  # 50% cheaper
    
    # Complex analysis → use smart model
    return "models/gemini-2.0-flash-exp"


# ==================== COST TRACKING ====================

class CostTracker:
    """Track costs with model-specific pricing"""
    
    PRICING = {
        "models/gemini-2.0-flash-exp": 0.00001,  # per token (estimate)
        "models/gemini-1.5-flash": 0.000005      # 50% cheaper
    }
    
    def __init__(self):
        self.total_cost = 0.0
        self.call_count = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.calls_by_model = {}
    
    def add_call(self, model: str, tokens: int, cached: bool = False):
        """Track API call cost"""
        if cached:
            self.cache_hits += 1
            cost = 0  # Cached = free
        else:
            self.cache_misses += 1
            cost = tokens * self.PRICING.get(model, 0.00001)
            self.total_cost += cost
        
        self.call_count += 1
        self.calls_by_model[model] = self.calls_by_model.get(model, 0) + 1
        
        print(f"Cost: ${cost:.6f} | Total: ${self.total_cost:.6f} | Model: {model.split('/')[-1]}")
    
    def get_summary(self) -> Dict[str, Any]:
        cache_rate = (self.cache_hits / max(1, self.call_count)) * 100
        
        return {
            "total_cost": round(self.total_cost, 6),
            "calls": self.call_count,
            "cache_hit_rate": f"{cache_rate:.1f}%",
            "savings_from_cache": round(self.cache_hits * 0.01, 4),
            "models_used": self.calls_by_model
        }


# ==================== FUNCTION DECLARATIONS ====================

# Compact function declarations (token optimized)
analyze_function = FunctionDeclaration(
    name="analyze_code_submission",
    description="Analyze code, run tests, detect patterns, give feedback",
    parameters={
        "type": "object",
        "properties": {
            "problem_id": {"type": "string", "description": "Problem ID"},
            "user_code": {"type": "string", "description": "User's code"},
            "language": {"type": "string", "description": "python/javascript"},
            "user_id": {"type": "string", "description": "User ID"}
        },
        "required": ["problem_id", "user_code"]
    }
)

recommend_function = FunctionDeclaration(
    name="get_recommended_problem",
    description="Get next problem based on weaknesses",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "User ID"},
            "difficulty_level": {"type": "string", "description": "easy/medium/hard"}
        }
    }
)

progress_function = FunctionDeclaration(
    name="track_user_progress",
    description="Update weakness scores after submission",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "problem_id": {"type": "string"},
            "detected_patterns": {"type": "array", "items": {"type": "string"}},
            "time_taken_minutes": {"type": "number"},
            "attempts_count": {"type": "integer"},
            "solved_correctly": {"type": "boolean"}
        },
        "required": ["user_id", "problem_id", "detected_patterns", "time_taken_minutes", "attempts_count", "solved_correctly"]
    }
)

codementor_tool = Tool(function_declarations=[analyze_function, recommend_function, progress_function])


# ==================== OPTIMIZED AGENT ====================

class OptimizedCodeMentorAgent:
    """Agent with caching, token optimization, and dual model routing"""
    
    def __init__(self):
        self.cache = ResponseCache(ttl_seconds=300)
        self.cost_tracker = CostTracker()
        self.models = {
            "models/gemini-2.0-flash-exp": genai.GenerativeModel(
                model_name="models/gemini-2.0-flash-exp",
                tools=[codementor_tool],
                system_instruction=OPTIMIZED_SYSTEM_PROMPT
            ),
            "models/gemini-1.5-flash": genai.GenerativeModel(
                model_name="models/gemini-1.5-flash",
                tools=[codementor_tool],
                system_instruction=OPTIMIZED_SYSTEM_PROMPT
            )
        }
        self.chat = None
        self.current_model = "models/gemini-2.0-flash-exp"
    
    def start_conversation(self):
        self.chat = self.models[self.current_model].start_chat()
        return "CodeMentor AI ready! (Optimized for speed and cost)"
    
    def _execute_function_call(self, function_call) -> Any:
        """Execute function with caching"""
        function_name = function_call.name
        function_args = dict(function_call.args)
        
        # Check cache first
        cached_result = self.cache.get(function_name, function_args)
        if cached_result:
            self.cost_tracker.add_call(self.current_model, tokens=0, cached=True)
            return cached_result
        
        # Cache miss - execute function
        if function_name == "analyze_code_submission":
            result = analyze_code_submission(**function_args)
        elif function_name == "get_recommended_problem":
            result = get_recommended_problem(**function_args)
        elif function_name == "track_user_progress":
            result = track_user_progress(**function_args)
        else:
            return {"error": f"Unknown function: {function_name}"}
        
        result_dict = result.model_dump()
        
        # Cache the result
        self.cache.set(function_name, function_args, result_dict)
        
        # Track cost (estimate 300 tokens avg with optimization)
        self.cost_tracker.add_call(self.current_model, tokens=300, cached=False)
        
        return result_dict
    
    def send_message(self, user_message: str) -> str:
        """Send message with optimizations"""
        if not self.chat:
            self.start_conversation()
        
        start_time = time.time()
        
        try:
            # Initial API call
            response = self.chat.send_message(user_message)
            self.cost_tracker.add_call(self.current_model, tokens=200, cached=False)
            
            # Handle function calling
            while response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                
                # OPTIMIZATION 3: Route to appropriate model
                optimal_model = choose_model(function_call.name)
                if optimal_model != self.current_model:
                    print(f"Switching to {optimal_model.split('/')[-1]}")
                    self.current_model = optimal_model
                    self.chat = self.models[optimal_model].start_chat()
                
                print(f"Calling: {function_call.name}")
                
                # Execute with caching
                function_result = self._execute_function_call(function_call)
                
                # Send result back
                response = self.chat.send_message(
                    content_types.to_content({
                        "function_response": {
                            "name": function_call.name,
                            "response": function_result
                        }
                    })
                )
            
            elapsed = time.time() - start_time
            print(f" Response time: {elapsed:.2f}s")
            print(f" {self.cost_tracker.get_summary()}")
            
            return response.text
        
        except Exception as e:
            import traceback
            print(f"Error: {traceback.format_exc()}")
            return f"Error: {str(e)}"


# ==================== DEMO ====================

if __name__ == "__main__":
    print("=== OPTIMIZED CodeMentor Agent ===\n")
    
    agent = OptimizedCodeMentorAgent()
    agent.start_conversation()
    
    # Test 1: First request (cache miss)
    print("\n--- Test 1: First request ---")
    response = agent.send_message("What problem should I practice next?")
    print(f"Response: {response[:100]}...\n")
    
    # Test 2: Same request (cache hit)
    print("\n--- Test 2: Same request (should use cache) ---")
    response = agent.send_message("What problem should I practice next?")
    print(f"Response: {response[:100]}...\n")
    
    # Test 3: Different request
    print("\n--- Test 3: Different request ---")
    response = agent.send_message("What problem should I practice for medium difficulty?")
    print(f"Response: {response[:100]}...\n")
    
    print("\n=== Final Cost Summary ===")
    print(agent.cost_tracker.get_summary())