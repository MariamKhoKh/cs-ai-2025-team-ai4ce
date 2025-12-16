import os
import time
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel, Field, validator

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ==================== ENHANCED TELEMETRY & LOGGING ====================

os.makedirs("logs", exist_ok=True)

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('logs/agent_audit.log'),
        logging.FileHandler('logs/telemetry.log')  # Separate telemetry log
    ]
)

logger = logging.getLogger(__name__)
telemetry_logger = logging.getLogger('telemetry')

def log_audit(event_type: str, details: Dict[str, Any]):
    """Log all agent actions for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    logger.info(json.dumps(log_entry))

def log_telemetry(
    request_id: str,
    user_id: str,
    query_type: str,
    latency_ms: float,
    success: bool,
    cost_usd: float = 0.0,
    model_used: str = "gemini-2.0-flash-exp",
    cache_hit: bool = False,
    error_type: Optional[str] = None,
    **kwargs
):
    """
    Log detailed telemetry for every request.
    This is what Lab 10 requires for production monitoring.
    """
    telemetry_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_id": request_id,
        "user_id": user_id,
        "query_type": query_type,
        "latency_ms": round(latency_ms, 2),
        "success": success,
        "cost_usd": round(cost_usd, 6),
        "model_used": model_used,
        "cache_hit": cache_hit,
        "error_type": error_type,
        **kwargs  # Additional fields like response_length, function_called, etc.
    }
    telemetry_logger.info(json.dumps(telemetry_entry))


# ==================== INPUT VALIDATION ====================

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


# ==================== CIRCUIT BREAKER ====================

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


# ==================== AUTHORIZATION ====================

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


# ==================== RETRY + TIMEOUTS ====================

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


# ==================== COST TRACKING ====================

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


# ==================== PRODUCTION AGENT WITH FULL TELEMETRY ====================

class ProductionAgent:
    """Production agent with all 8 safety features + comprehensive telemetry"""
    
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
        Send message with full safety features and telemetry.
        NEVER crashes - always returns structured response.
        """
        # Generate unique request ID for tracing
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        # Initialize telemetry variables
        query_type = "unknown"
        function_called = None
        response_length = 0
        error_type = None
        
        try:
            # Check cost limit BEFORE calling API
            if self.cost_tracker.total_cost >= self.cost_tracker.cost_limit:
                error_type = "cost_limit_exceeded"
                log_telemetry(
                    request_id=request_id,
                    user_id=user_id,
                    query_type="cost_limit_check",
                    latency_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error_type=error_type
                )
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
            self.cost_tracker.add_cost(0.002, "gemini_api_call")  # More realistic cost
            
            # Check for function calls
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                function_called = function_call.name
                
                # Determine query type from function name
                if "analyze" in function_called:
                    query_type = "code_analysis"
                elif "recommend" in function_called:
                    query_type = "recommendation"
                elif "progress" in function_called:
                    query_type = "progress_tracking"
                
                # AUTHORIZATION CHECK
                if not check_authorization(user_id, function_call.name):
                    error_type = "unauthorized"
                    log_telemetry(
                        request_id=request_id,
                        user_id=user_id,
                        query_type=query_type,
                        latency_ms=(time.time() - start_time) * 1000,
                        success=False,
                        error_type=error_type,
                        function_called=function_called
                    )
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
                    error_type = "validation_error"
                    log_audit("validation_error", {"error": str(validation_error)})
                    log_telemetry(
                        request_id=request_id,
                        user_id=user_id,
                        query_type=query_type,
                        latency_ms=(time.time() - start_time) * 1000,
                        success=False,
                        error_type=error_type,
                        function_called=function_called
                    )
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
            else:
                query_type = "conversational"
            
            # Calculate final metrics
            execution_time = time.time() - start_time
            response_length = len(response.text) if hasattr(response, 'text') else 0
            
            # LOG SUCCESSFUL REQUEST TELEMETRY
            log_telemetry(
                request_id=request_id,
                user_id=user_id,
                query_type=query_type,
                latency_ms=execution_time * 1000,
                success=True,
                cost_usd=self.cost_tracker.total_cost / max(1, self.cost_tracker.call_count),
                model_used="gemini-2.0-flash-exp",
                cache_hit=False,  # Set to True if using cache
                function_called=function_called,
                response_length=response_length
            )
            
            log_audit("successful_request", {
                "request_id": request_id,
                "user_id": user_id,
                "execution_time": execution_time,
                "cost": self.cost_tracker.total_cost
            })
            
            return {
                "success": True,
                "message": response.text,
                "execution_time": round(execution_time, 2),
                "cost_summary": self.cost_tracker.get_summary(),
                "request_id": request_id
            }
        
        except Exception as e:
            # NEVER CRASH - always return friendly message
            execution_time = time.time() - start_time
            error_type = type(e).__name__
            
            # LOG ERROR TELEMETRY
            log_telemetry(
                request_id=request_id,
                user_id=user_id,
                query_type=query_type,
                latency_ms=execution_time * 1000,
                success=False,
                error_type=error_type,
                function_called=function_called
            )
            
            log_audit("error", {
                "request_id": request_id,
                "user_id": user_id,
                "error_type": error_type,
                "error_message": str(e),
                "execution_time": execution_time
            })
            
            return {
                "success": False,
                "message": "I encountered an issue processing your request. Please try again.",
                "error_type": error_type,
                "execution_time": round(execution_time, 2),
                "cost_summary": self.cost_tracker.get_summary(),
                "request_id": request_id
            }
    
    def _execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute function with error handling"""
        tool_func = self.tools.get(function_name)
        if not tool_func:
            raise ValueError(f"Unknown function: {function_name}")
        
        result = tool_func(**arguments)
        return result.model_dump()


# ==================== TELEMETRY ANALYSIS HELPER ====================

def analyze_telemetry_logs(log_file: str = "logs/telemetry.log", hours: int = 24):
    """
    Analyze telemetry logs to get system metrics.
    Useful for monitoring dashboard.
    """
    from collections import Counter
    from datetime import timedelta
    
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    total_requests = 0
    successful_requests = 0
    latencies = []
    costs = []
    error_types = Counter()
    query_types = Counter()
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    timestamp = datetime.fromisoformat(entry['timestamp'])
                    
                    if timestamp > cutoff_time:
                        total_requests += 1
                        
                        if entry['success']:
                            successful_requests += 1
                        else:
                            error_types[entry.get('error_type', 'unknown')] += 1
                        
                        latencies.append(entry['latency_ms'])
                        costs.append(entry.get('cost_usd', 0))
                        query_types[entry['query_type']] += 1
                        
                except json.JSONDecodeError:
                    continue
        
        if total_requests == 0:
            print(f"No telemetry data found in last {hours} hours")
            return
        
        # Calculate statistics
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
        success_rate = (successful_requests / total_requests) * 100
        error_rate = ((total_requests - successful_requests) / total_requests) * 100
        
        print(f"\n{'='*60}")
        print(f"TELEMETRY ANALYSIS (Last {hours} hours)")
        print(f"{'='*60}")
        print(f"\n📊 REQUEST METRICS:")
        print(f"  Total Requests:    {total_requests}")
        print(f"  Successful:        {successful_requests} ({success_rate:.1f}%)")
        print(f"  Failed:            {total_requests - successful_requests} ({error_rate:.1f}%)")
        
        print(f"\n⏱️  LATENCY:")
        print(f"  Average:           {avg_latency:.0f}ms")
        print(f"  P95:               {p95_latency:.0f}ms")
        
        print(f"\n💰 COST:")
        print(f"  Total:             ${sum(costs):.4f}")
        print(f"  Average/query:     ${sum(costs)/len(costs):.6f}")
        
        print(f"\n📈 QUERY TYPES:")
        for qtype, count in query_types.most_common():
            print(f"  {qtype:20} {count:4} ({count/total_requests*100:.1f}%)")
        
        if error_types:
            print(f"\n❌ ERROR TYPES:")
            for etype, count in error_types.most_common():
                print(f"  {etype:20} {count:4} ({count/total_requests*100:.1f}%)")
        
        print(f"\n{'='*60}\n")
        
    except FileNotFoundError:
        print(f"Telemetry log file not found: {log_file}")


if __name__ == "__main__":
    print("Testing Production Agent with Telemetry\n")
    
    agent = ProductionAgent(cost_limit=0.50)
    
    print("Test 1: Normal request")
    result = agent.send_message("What problem should I practice next?", user_id="user_001")
    print(f"Success: {result['success']}")
    print(f"Request ID: {result.get('request_id')}")
    print(f"Cost: ${result['cost_summary']['total_cost']}\n")
    
    print("Test 2: Code analysis")
    result = agent.send_message(
        "Analyze this code: def two_sum(nums, target):\n    for i in range(len(nums)):\n        return [0, 1]",
        user_id="user_001"
    )
    print(f"Success: {result['success']}")
    print(f"Request ID: {result.get('request_id')}\n")
    
    print("\nCheck logs/telemetry.log for detailed metrics")
    print("Check logs/agent_audit.log for audit trail\n")
    
    # Analyze telemetry
    print("Analyzing telemetry from last 24 hours:")
    analyze_telemetry_logs()
