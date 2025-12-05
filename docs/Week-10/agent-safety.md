# Agent Safety Documentation

## 1. Permissions Matrix

| Tool Name | Permission Level | Who Can Use | Justification |
|-----------|-----------------|-------------|---------------|
| `analyze_code_submission` | WRITE | Regular users, Admins | Modifies user's submission history and weakness profile |
| `get_recommended_problem` | READ | All users | Only reads data, no modifications |
| `track_user_progress` | WRITE | Regular users, Admins | Updates user's progress metrics and scores |

### User Roles
- **READ**: Can only view problems and recommendations
- **WRITE**: Can submit code and track progress (regular users)
- **ADMIN**: Full access to all operations

### Authorization Logic
```python
# Hierarchy: READ (1) < WRITE (2) < ADMIN (3)
# User must have permission >= required permission
```

---

## 2. Failure Scenarios

### Scenario 1: Timeout (API Takes Too Long)

**Trigger**: External API call exceeds 5 seconds (or Gemini exceeds 30 seconds)

**Detection**: 
```python
@timeout_decorator(5)  # Raises TimeoutError after 5s
def call_external_api(...)
```

**Handling**:
1. Timeout decorator raises `TimeoutError`
2. Retry logic catches it and retries (up to 3 attempts with exponential backoff: 1s → 2s → 4s)
3. If all retries fail, return user-friendly error

**User Impact**: 
- Message: "I encountered an issue processing your request. Please try again."
- No raw error details exposed
- Request logged for debugging

**Fallback**: No partial results returned; user must retry entire request

---

### Scenario 2: Infinite Loop (Max Iterations)

**Trigger**: Not applicable - we use **direct function calling**, not a ReAct loop

**Why Not Applicable**: 
- CodeMentor uses single-step function execution
- Gemini decides which function to call, executes once, returns result
- No iterative loops = no risk of infinite loops

**If We Had a ReAct Agent**:
- Would set `max_iterations=5`
- Would return: "I couldn't complete your request within the time limit"

---

### Scenario 3: Unauthorized Access (User Tries Restricted Tool)

**Trigger**: User without WRITE permission tries to call `analyze_code_submission`

**Detection**:
```python
if not check_authorization(user_id, tool_name):
    # Block execution
```

**Handling**:
1. Authorization check runs BEFORE tool execution
2. If unauthorized, execution stops immediately
3. Attempt logged to audit log with user_id and tool name

**User Impact**:
- Message: "You don't have permission to use analyze_code_submission"
- No sensitive details about why or how auth works
- User sees generic permission error

**Fallback**: No execution attempted; request rejected cleanly

---

### Scenario 4: External API Broken (Circuit Breaker)

**Trigger**: A tool (e.g., `analyze_code_submission`) fails 5 times in a row

**Detection**:
```python
class CircuitBreaker:
    if self.failure_count >= 5:
        self.state = "open"
```

**Handling**:
1. After 5 failures, circuit breaker opens
2. For next 60 seconds, ALL calls to that tool fail immediately (no retry)
3. After 60s, circuit enters "half-open" state (tries one request)
4. If successful → circuit closes; if fails → stays open for another 60s

**User Impact**:
- Message: "I encountered an issue processing your request. Please try again."
- User doesn't know circuit is open (internal detail)
- Prevents wasting money on known-broken services

**Fallback**: 
- Other tools still work (circuit breaker is per-tool)
- User can try different operations
- After 60s cooldown, tool becomes available again

---

## 3. Cost Protection

**Per-Request Limit**: $1.00 (configurable)

**Behavior**:
- Before each API call, agent checks: `if total_cost >= cost_limit`
- If limit reached, stops immediately
- Returns: "Cost limit reached. Please try again later."

**Tracking**:
- Every API call logged with cost estimate
- Total accumulated across session
- Cost summary returned in every response

---

## 4. Audit Logging

**What's Logged** (to `logs/agent_audit.log`):
- Timestamp
- Event type (api_call, authorization_check, cost_tracking, error)
- User ID
- Tool name
- Success/failure
- Cost and execution time

**What's NOT Logged**:
- User's submitted code (too large, may contain sensitive info)
- API keys
- Passwords
- Raw error stack traces (only error type + message)

**Format**: JSON for easy parsing
```json
{"timestamp": "2024-12-04T10:30:00", "event_type": "authorization_check", "details": {...}}
```

---

## 5. Error Handling Strategy

**Philosophy**: Agent NEVER crashes - always returns structured response

**Implementation**:
```python
try:
    # Execute agent logic
except Exception as e:
    # Log error details
    log_audit("error", {...})
    
    # Return friendly message
    return {
        "success": False,
        "message": "I encountered an issue...",
        "error_type": type(e).__name__
    }
```

**User Experience**:
- Always gets a response (never HTTP 500)
- Sees friendly error message
- Can retry immediately
- Support team can debug from logs

---

## 6. Testing Checklist

- [x] Authorization blocks unauthorized users
- [x] Timeout stops long-running calls
- [x] Retry logic attempts 3 times with backoff
- [x] Circuit breaker opens after 5 failures
- [x] Cost limit stops execution
- [x] All errors return friendly messages
- [x] Audit log captures all events
- [x] Input validation rejects malformed data