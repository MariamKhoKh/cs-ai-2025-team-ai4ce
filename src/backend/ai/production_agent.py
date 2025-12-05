import os
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any
from functools import wraps
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel, Field, validator

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ==================== FEATURE 1: AUDIT LOGGING ====================

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/agent_audit.log',
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

def log_audit(event_type: str, details: Dict[str, Any]):
    """Log all agent actions for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    logger.info(json.dumps(log_entry))


# ==================== FEATURE 2: INPUT VALIDATION ====================

class AnalyzeCodeInput(BaseModel):
    problem_id: str = Field(..., min_length=1, max_length=100)
    user_code: str = Field(..., min_length=1, max_length=10000)
    language: str = Field(default="python")
    user_id: str = Field(default="user_001")
    
    @validator('problem_id')
    def validate_problem_id(cls, v):
        if not v.strip():
            raise ValueError("problem_id cannot be empty")
        return v.strip()


# ==================== FEATURE 3: CIRCUIT BREAKER ====================

class CircuitBreaker:
    """Circuit breaker per tool to prevent cascading failures"""
    
    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        
        # If circuit is open, check if timeout expired
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half_open"
                log_audit("circuit_breaker", {"state": "half_open", "tool": func.__name__})
            else:
                raise Exception(f"Circuit breaker OPEN for {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            # Success resets circuit
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
                log_audit("circuit_breaker", {"state": "closed", "tool": func.__name__})
            return result
        
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                log_audit("circuit_breaker", {
                    "state": "open",
                    "tool": func.__name__,
                    "failures": self.failure_count
                })
            raise e


# ==================== FEATURE 4: AUTHORIZATION ====================

class Permission:
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

TOOL_PERMISSIONS = {
    "analyze_code_submission": Permission.WRITE,
    "get_recommended_problem": Permission.READ,
    "track_user_progress": Permission.WRITE
}

USER_ROLES = {
    "user_001": Permission.WRITE,
    "admin_001": Permission.ADMIN
}

def check_authorization(user_id: str, tool_name: str) -> bool:
    """Check if user has permission to use tool"""
    required_permission = TOOL_PERMISSIONS.get(tool_name, Permission.ADMIN)
    user_permission = USER_ROLES.get(user_id, Permission.READ)
    
    permission_hierarchy = {
        Permission.READ: 1,
        Permission.WRITE: 2,
        Permission.ADMIN: 3
    }
    
    authorized = permission_hierarchy[user_permission] >= permission_hierarchy[required_permission]
    
    log_audit("authorization_check", {
        "user_id": user_id,
        "tool": tool_name,
        "required": required_permission,
        "user_has": user_permission,
        "authorized": authorized
    })
    
    return authorized


# ==================== FEATURE 5 & 6: RETRY + TIMEOUTS ====================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type((TimeoutError, ConnectionError))
)
def call_with_retry(func, *args, timeout_seconds=5, **kwargs):
    """Call function with timeout and retry logic"""
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError(f"{func.__name__} exceeded {timeout_seconds}s timeout")
    
    # Set alarm (Unix-like systems only)
    try:
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        
        result = func(*args, **kwargs)
        
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
        return result
    except AttributeError:
        # Windows doesn't support signal.SIGALRM
        # Fallback to simple execution
        return func(*args, **kwargs)


# ==================== FEATURE 7: COST TRACKING ====================

class CostTracker:
    """Track API costs and enforce limits"""
    
    def __init__(self, cost_limit=1.0):
        self.total_cost = 0.0
        self.cost_limit = cost_limit
        self.call_count = 0
    
    def add_cost(self, cost: float, operation: str):
        """Add cost and check limit"""
        self.total_cost += cost
        self.call_count += 1
        
        log_audit("cost_tracking", {
            "operation": operation,
            "cost": cost,
            "total_cost": self.total_cost,
            "call_count": self.call_count
        })
        
        if self.total_cost >= self.cost_limit:
            raise Exception(f"Cost limit exceeded: ${self.total_cost:.4f} >= ${self.cost_limit}")
    
    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_cost": round(self.total_cost, 4),
            "call_count": self.call_count,
            "average_cost": round(self.total_cost / max(1, self.call_count), 4)
        }


# ==================== FEATURE 8: ERROR HANDLING ====================

class ProductionAgent:
    """Production agent with all 8 safety features"""
    
    def __init__(self, cost_limit=1.0):
        self.model = genai.GenerativeModel(model_name="models/gemini-2.0-flash-exp")
        self.chat = None
        self.cost_tracker = CostTracker(cost_limit)
        self.circuit_breakers = {}
        
        # Import tools
        from src.backend.functions.tools import (
            analyze_code_submission,
            get_recommended_problem,
            track_user_progress
        )
        self.tools = {
            "analyze_code_submission": analyze_code_submission,
            "get_recommended_problem": get_recommended_problem,
            "track_user_progress": track_user_progress
        }
    
    def _get_circuit_breaker(self, tool_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for tool"""
        if tool_name not in self.circuit_breakers:
            self.circuit_breakers[tool_name] = CircuitBreaker()
        return self.circuit_breakers[tool_name]
    
    def send_message(self, user_message: str, user_id: str = "user_001") -> Dict[str, Any]:
        """
        Send message with full safety features.
        NEVER crashes - always returns structured response.
        """
        start_time = time.time()
        
        try:
            # Check cost limit BEFORE calling API
            if self.cost_tracker.total_cost >= self.cost_tracker.cost_limit:
                return {
                    "success": False,
                    "message": "Cost limit reached. Please try again later.",
                    "cost_summary": self.cost_tracker.get_summary()
                }
            
            # Start chat if needed
            if not self.chat:
                self.chat = self.model.start_chat()
            
            # Call Gemini with retry and timeout (30s for LLM)
            response = call_with_retry(self.chat.send_message, user_message, timeout_seconds=30)
            
            # Track cost
            self.cost_tracker.add_cost(0.01, "gemini_api_call")
            
            # Check for function calls
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                
                # AUTHORIZATION CHECK
                if not check_authorization(user_id, function_call.name):
                    return {
                        "success": False,
                        "message": f"You don't have permission to use {function_call.name}",
                        "cost_summary": self.cost_tracker.get_summary()
                    }
                
                # INPUT VALIDATION
                try:
                    if function_call.name == "analyze_code_submission":
                        validated = AnalyzeCodeInput(**dict(function_call.args))
                except Exception as validation_error:
                    log_audit("validation_error", {"error": str(validation_error)})
                    return {
                        "success": False,
                        "message": f"Invalid input: {validation_error}",
                        "cost_summary": self.cost_tracker.get_summary()
                    }
                
                # Execute with CIRCUIT BREAKER
                circuit_breaker = self._get_circuit_breaker(function_call.name)
                function_result = circuit_breaker.call(
                    self._execute_function,
                    function_call.name,
                    dict(function_call.args)
                )
                
                # Send result back
                response = self.chat.send_message({
                    "function_response": {
                        "name": function_call.name,
                        "response": function_result
                    }
                })
            
            execution_time = time.time() - start_time
            
            log_audit("successful_request", {
                "user_id": user_id,
                "execution_time": execution_time,
                "cost": self.cost_tracker.total_cost
            })
            
            return {
                "success": True,
                "message": response.text,
                "execution_time": round(execution_time, 2),
                "cost_summary": self.cost_tracker.get_summary()
            }
        
        except Exception as e:
            # NEVER CRASH - always return friendly message
            execution_time = time.time() - start_time
            
            log_audit("error", {
                "user_id": user_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "execution_time": execution_time
            })
            
            return {
                "success": False,
                "message": "I encountered an issue processing your request. Please try again.",
                "error_type": type(e).__name__,
                "execution_time": round(execution_time, 2),
                "cost_summary": self.cost_tracker.get_summary()
            }
    
    def _execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute function with error handling"""
        tool_func = self.tools.get(function_name)
        if not tool_func:
            raise ValueError(f"Unknown function: {function_name}")
        
        result = tool_func(**arguments)
        return result.model_dump()


if __name__ == "__main__":
    print("Testing Production Agent\n")
    
    agent = ProductionAgent(cost_limit=0.50)
    
    print("Test 1: Normal request")
    result = agent.send_message("What problem should I practice next?", user_id="user_001")
    print(f"Success: {result['success']}")
    print(f"Cost: ${result['cost_summary']['total_cost']}\n")
    
    print("Check logs/agent_audit.log for audit trail")