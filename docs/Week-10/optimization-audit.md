# Optimization Audit Report
**Project:** CodeMentor AI - Technical Interview Prep Platform  
**Date:** December 4, 2024  
**Audit Period:** Week 10 - Production Optimization Lab  
**Team:** AI4ce

---

## Executive Summary

This audit analyzes CodeMentor AI's current cost structure and identifies optimization opportunities to reduce operational expenses by 80%+ while maintaining quality. Our analysis reveals that **Judge0 integration poses the largest cost risk** ($3,600/month at scale), while Gemini API costs remain negligible ($9.60/month).

**Key Findings:**
- Current monthly cost: **$9.60** (1,000 users, Gemini only)
- Projected with Judge0: **$3,610/month** (94% increase from Judge0)
- Optimization potential: **$3,490/month savings (97% reduction)**
- Top opportunity: Self-hosted Judge0 → $3,550/month savings

---

## Section 1: Current State Analysis

### 1.1 API Call Inventory

| Component | Endpoint/Model | Calls per User Session | Monthly Volume (1K users) | Current Status |
|-----------|----------------|------------------------|---------------------------|----------------|
| **Gemini API** | gemini-2.5-flash | 10 requests | 300,000 requests | ✅ Active |
| **Judge0 API** | Submissions endpoint | 30 executions (3 tests × 10 problems) | 900,000 executions | ⏳ Planned Week 7 |
| **Function Calls** | analyze_code_submission | 5 calls | 150,000 calls | ✅ Active |
| **Function Calls** | get_recommended_problem | 3 calls | 90,000 calls | ✅ Active |
| **Function Calls** | track_user_progress | 2 calls | 60,000 calls | ✅ Active |

**Notes:**
- Each Gemini request triggers 0-3 function calls via function calling loop
- Judge0 calls happen inside `analyze_code_submission()` for test execution
- Current implementation uses **mock test data** (no Judge0 calls yet)

### 1.2 Baseline Cost Calculation

#### **Current Costs (Mock Data Only)**

**Gemini API Costs:**
- **Model:** gemini-2.5-flash
- **Pricing:** $0.00001875/1K input tokens, $0.000075/1K output tokens
- **Average tokens per request:** 450 input + 300 output = 750 total tokens
- **Cost per request:** (450 × $0.00001875/1000) + (300 × $0.000075/1000) = **$0.000032**

**Monthly projection (1,000 users × 10 requests/day × 30 days):**
- Total requests: 300,000
- **Total cost: $9.60/month**

**Function execution costs:** $0 (runs on local compute, mock data lookups)

**Total current monthly cost: $9.60**

---

#### **Projected Costs WITH Judge0 (Week 7+)**

**Judge0 Cloud API Costs:**
- **Pricing:** $0.004 per execution
- **Test cases per submission:** 3 average
- **Submissions per user/day:** 10 problems
- **Monthly executions:** 1,000 users × 10 problems/day × 3 tests × 30 days = **900,000 executions**
- **Judge0 monthly cost:** 900,000 × $0.004 = **$3,600/month** 🚨

**Total projected cost with Judge0:**
- Gemini: $9.60
- Judge0: $3,600
- **Total: $3,609.60/month**

**Cost breakdown by percentage:**
- Judge0: 99.7%
- Gemini: 0.3%

---

### 1.3 Latency Measurements

| Component | p50 (median) | p95 | p99 | Average | Target | Status |
|-----------|--------------|-----|-----|---------|--------|--------|
| **analyze_code_submission** | 45ms | 51ms | 55ms | 46ms | <500ms | ✅ PASS |
| **get_recommended_problem** | 12ms | 14ms | 15ms | 12ms | <500ms | ✅ PASS |
| **track_user_progress** | 8ms | 9ms | 10ms | 8ms | <500ms | ✅ PASS |
| **Gemini API call** | ~800ms* | ~1200ms* | ~1500ms* | ~900ms* | <2000ms | ✅ PASS |

*Estimated based on typical Gemini Flash latency; not measured in current tests (mock data only)

**Notes:**
- Current measurements are for **mock data only** (no real API calls in tests)
- Expected Judge0 latency: **500-2000ms per execution** (not yet measured)
- Function execution is fast (8-46ms), API calls will dominate latency

### 1.4 Current Caching Status

| Cache Type | Status | Impact |
|------------|--------|--------|
| **Prompt caching (Gemini)** | ❌ Not implemented | System prompts + function declarations sent every request |
| **Response caching** | ❌ Not implemented | Identical queries hit API every time |
| **Judge0 result caching** | ❌ Not implemented | Same code submissions re-executed |
| **In-memory caching** | ❌ Not implemented | No cachetools, Redis, or similar |

**Current approach:** Every request is a fresh API call with no caching layer.

---

## Section 2: Optimization Opportunities

### Opportunity 1: Implement Judge0 Result Caching 🎯 **HIGHEST IMPACT**

**Description:**  
Cache Judge0 execution results based on hash of (problem_id + user_code + language). Identical code submissions return cached results instead of re-executing.

**Projected Savings:**
- Assumption: 30% of submissions are duplicates (common beginner mistakes)
- Current cost: $3,600/month
- After caching: $2,520/month
- **Monthly savings: $1,080 (30% reduction)**

**Effort Estimate:** Medium (1-2 days)
- Add Redis or in-memory cache with 24-hour TTL
- Hash user_code + problem_id as cache key
- Check cache before calling Judge0 API

**Implementation Notes:**
```python
import hashlib
from cachetools import TTLCache

judge0_cache = TTLCache(maxsize=10000, ttl=86400)  # 24 hour TTL

def get_cache_key(problem_id: str, user_code: str, language: str) -> str:
    content = f"{problem_id}:{user_code}:{language}"
    return hashlib.sha256(content.encode()).hexdigest()

# In analyze_code_submission():
cache_key = get_cache_key(problem_id, user_code, language)
if cache_key in judge0_cache:
    return judge0_cache[cache_key]  # Return cached results

# After Judge0 execution:
judge0_cache[cache_key] = test_results
```

---

### Opportunity 2: Self-Host Judge0 on AWS EC2 🎯 **HIGHEST SAVINGS**

**Description:**  
Deploy Judge0 CE (open-source) on AWS EC2 instead of using cloud API. Pay fixed monthly compute cost instead of per-execution pricing.

**Projected Savings:**
- Current cost: $3,600/month (cloud API)
- EC2 t3.medium cost: ~$30/month (reserved instance)
- Docker setup + maintenance: ~$20/month (developer time)
- **New total: $50/month**
- **Monthly savings: $3,550 (98.6% reduction)** 🎉

**Effort Estimate:** High (3-5 days initial setup, ongoing maintenance)
- Set up EC2 instance with Docker
- Deploy Judge0 CE containers
- Configure security groups
- Monitor performance and scale

**Implementation Notes:**
- Judge0 CE GitHub: https://github.com/judge0/judge0
- Requires: Redis, PostgreSQL, Judge0 server, Judge0 worker
- Consider AWS ECS for easier scaling

**Risk Mitigation:**
- Start with cloud API, migrate to self-hosted when hitting 100+ users/day
- Keep cloud API as fallback for high-load periods

---

### Opportunity 3: Implement Gemini Prompt Caching

**Description:**  
Use Gemini's prompt caching feature to cache system instructions and function declarations. Reduces input token costs by 90% for repeated prompts.

**Projected Savings:**
- Current Gemini cost: $9.60/month
- Function declarations: ~200 tokens (sent with every request)
- With caching: Save 90% on cached content → $8.64/month savings
- **Monthly savings: $8.64 (90% reduction of Gemini costs)**

**Effort Estimate:** Low (2-4 hours)
- Add `cached_content` parameter to Gemini API calls
- Cache function declarations for 1 hour
- Update agent initialization

**Implementation Notes:**
```python
# In agent.py __init__:
from google.generativeai import caching

# Create cached content with function declarations
cached_functions = caching.CachedContent.create(
    model='models/gemini-2.5-flash',
    system_instruction="You are CodeMentor AI...",
    tools=[codementor_tool],
    ttl=3600  # 1 hour cache
)

# Use cached content in model
self.model = genai.GenerativeModel.from_cached_content(
    cached_content=cached_functions
)
```

---

### Opportunity 4: Batch Test Case Execution

**Description:**  
Send all test cases for a problem in a single Judge0 batch request instead of 3 separate requests. Reduces API call overhead.

**Projected Savings:**
- Current: 3 API calls per submission × $0.004 = $0.012
- Batched: 1 API call per submission × $0.004 = $0.004
- **Savings per submission: $0.008 (67% reduction)**
- **Monthly savings: $2,400** (if still using cloud API)

**Effort Estimate:** Medium (1 day)
- Use Judge0 batch submissions endpoint
- Parse batch results into individual TestResult objects

**Implementation Notes:**
```python
# Instead of:
for test_case in test_cases:
    result = judge0_api.submit(code, test_case)

# Use batch endpoint:
batch_response = judge0_api.submit_batch(code, test_cases)
results = parse_batch_results(batch_response)
```

**Note:** Only relevant if using cloud API. Not needed if self-hosting.

---

### Opportunity 5: Response Caching for Common Queries

**Description:**  
Cache entire Gemini responses for common user queries like "What should I practice next?" or "Analyze this two-sum solution."

**Projected Savings:**
- Assumption: 20% of queries are common patterns
- Current cost: $9.60/month
- After caching: $7.68/month
- **Monthly savings: $1.92 (20% reduction)**

**Effort Estimate:** Low (3-4 hours)
- Implement response cache with 1-hour TTL
- Hash user message as cache key
- Return cached response if available

**Implementation Notes:**
```python
from cachetools import TTLCache

response_cache = TTLCache(maxsize=1000, ttl=3600)

def send_message(self, user_message: str) -> str:
    # Check cache first
    cache_key = hashlib.md5(user_message.encode()).hexdigest()
    if cache_key in response_cache:
        return response_cache[cache_key]
    
    # Call API
    response = self.chat.send_message(user_message)
    
    # Cache response
    response_cache[cache_key] = response.text
    return response.text
```

---

### Opportunity 6: Smart Model Selection (Future)

**Description:**  
Use cheaper models (Gemini 1.5 Flash-8B) for simple queries, keep 2.5 Flash for complex analysis.

**Projected Savings:**
- Simple queries (40% of traffic): Use Flash-8B (50% cheaper)
- Complex queries (60%): Keep 2.5 Flash
- **Estimated savings: $1.92/month (20% of Gemini costs)**

**Effort Estimate:** Medium (2 days)
- Classify query complexity
- Route to appropriate model
- A/B test quality

**Implementation Notes:**
- Defer to Week 11+ (not critical for current scale)
- Current Gemini costs are already negligible

---

## Section 3: Implementation Plan

### 3.1 Prioritization Matrix

| Opportunity | Impact ($/month) | Effort | Priority | Timeline |
|-------------|------------------|--------|----------|----------|
| **Self-host Judge0** | $3,550 | High | 🔥 P0 | Week 11-12 |
| **Judge0 result caching** | $1,080 | Medium | 🔥 P0 | Week 10 (NOW) |
| **Batch test execution** | $2,400* | Medium | P1 | Week 10 |
| **Gemini prompt caching** | $8.64 | Low | P1 | Week 10 |
| **Response caching** | $1.92 | Low | P2 | Week 11 |
| **Smart model selection** | $1.92 | Medium | P3 | Week 12+ |

*Only if using cloud Judge0 API

### 3.2 Top 3 Selected for Week 10 Implementation

#### **Optimization #1: Judge0 Result Caching** 🎯
- **Owner:** [Assign team member]
- **Deadline:** December 10, 2024 (end of Week 10)
- **Success Criteria:**
  - Cache hit rate ≥ 25%
  - Latency reduction ≥ 500ms on cache hits
  - Cost reduction tracked in logs
- **Files to modify:**
  - `src/backend/functions/tools.py` (add caching logic)
  - `requirements.txt` (add `cachetools` or `redis`)
  - `src/utils/cache.py` (new file for cache utilities)

**Implementation steps:**
1. Install cachetools: `pip install cachetools`
2. Add cache initialization in tools.py
3. Wrap Judge0 calls with cache check
4. Add cache hit/miss logging
5. Test with identical submissions

---

#### **Optimization #2: Gemini Prompt Caching** 🎯
- **Owner:** [Assign team member]
- **Deadline:** December 10, 2024
- **Success Criteria:**
  - Input token cost reduced by 80%
  - No degradation in response quality
  - Cache refresh working correctly
- **Files to modify:**
  - `src/ai/agent.py` (add cached_content initialization)
  - Document cache TTL strategy

**Implementation steps:**
1. Research Gemini caching API docs
2. Update CodeMentorAgent.__init__() with cached content
3. Set 1-hour TTL for function declarations
4. Test cache refresh behavior
5. Monitor token usage via API logs

---

#### **Optimization #3: Batch Test Case Execution** 🎯
- **Owner:** [Assign team member]
- **Deadline:** December 10, 2024
- **Success Criteria:**
  - Single API call per submission (down from 3)
  - All test results still captured
  - Error handling robust
- **Files to modify:**
  - `src/backend/functions/tools.py` (_run_mock_tests function)
  - Update to use Judge0 batch endpoint when integrated

**Implementation steps:**
1. Review Judge0 batch API documentation
2. Refactor _run_mock_tests() to batch structure
3. Update TestResult parsing logic
4. Add error handling for batch failures
5. Test with 3+ test cases per problem

---

### 3.3 Success Metrics

**Baseline Metrics (Current):**
- Cost per 1K requests: $0.032 (Gemini only)
- Average latency: 46ms (mock data)
- Cache hit rate: 0% (no caching)

**Target Metrics (After Week 10):**
- Cost per 1K requests: $0.024 (25% reduction via caching)
- Average latency: 30ms (cache hits), 46ms (cache misses)
- Cache hit rate: ≥25% for Judge0, ≥15% for Gemini

**Long-term Targets (Week 12 with self-hosted Judge0):**
- Cost per 1K requests: $0.005 (95% reduction)
- Monthly cost at 1K users: $120/month (down from $3,610)

---

### 3.4 Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cache invalidation bugs | Medium | High | Implement cache versioning, add manual clear endpoint |
| Self-hosted Judge0 downtime | Low | High | Keep cloud API as fallback, monitor uptime |
| Cache memory overflow | Low | Medium | Set maxsize limits, use LRU eviction |
| Stale cached results | Medium | Low | Use short TTLs (1-24 hours), add cache-bust parameter |

---

## Section 4: Cost Calculator

### 4.1 Cost Projection Tool

**Google Sheets Calculator:** [Link to be added]

**Formula Structure:**
```
Monthly Cost = (Gemini_Requests × Gemini_Cost_Per_Request) + 
               (Judge0_Executions × Judge0_Cost_Per_Execution)

Where:
- Gemini_Cost_Per_Request = (Input_Tokens × $0.00001875/1000) + 
                              (Output_Tokens × $0.000075/1000)
- Judge0_Cost_Per_Execution = $0.004 (cloud) OR $0.0006 (self-hosted amortized)
```

### 4.2 Scenario Comparison

| Scenario | Users/Day | Monthly Gemini | Monthly Judge0 | Total/Month | vs Baseline |
|----------|-----------|----------------|----------------|-------------|-------------|
| **Current (Mock)** | 100 | $0.96 | $0 | $0.96 | Baseline |
| **Judge0 Cloud (No Optimization)** | 1,000 | $9.60 | $3,600 | $3,609.60 | +376,000% |
| **With Caching (30%)** | 1,000 | $6.72 | $2,520 | $2,526.72 | +263,000% |
| **With All Week 10 Optimizations** | 1,000 | $6.72 | $1,200 | $1,206.72 | +125,600% |
| **Self-Hosted Judge0** | 1,000 | $6.72 | $50 | $56.72 | +5,808% |
| **Fully Optimized** | 1,000 | $0.96 | $50 | $50.96 | +5,208% |

**Key Insight:** Self-hosting Judge0 is 98.6% cheaper than cloud API at scale.

### 4.3 Break-Even Analysis

**When does self-hosting Judge0 pay off?**

- Cloud API cost: $0.004 per execution
- Self-hosted fixed cost: $50/month
- Break-even point: $50 ÷ $0.004 = **12,500 executions/month**
- At 10 problems/day per user: **~42 active users/day**

**Recommendation:** Self-host when reaching 50+ daily active users (Week 11-12 timeframe).

---

## Appendix A: Code Examples

### Example 1: Judge0 Result Caching
```python
# src/utils/cache.py
import hashlib
from cachetools import TTLCache
from typing import Optional, List
from src.backend.models.function_models import TestResult

# Cache configuration
JUDGE0_CACHE = TTLCache(maxsize=10000, ttl=86400)  # 24 hours

def get_judge0_cache_key(problem_id: str, user_code: str, language: str) -> str:
    """Generate cache key for Judge0 results"""
    content = f"{problem_id}:{user_code}:{language}"
    return hashlib.sha256(content.encode()).hexdigest()

def get_cached_results(problem_id: str, user_code: str, language: str) -> Optional[List[TestResult]]:
    """Retrieve cached Judge0 results if available"""
    cache_key = get_judge0_cache_key(problem_id, user_code, language)
    return JUDGE0_CACHE.get(cache_key)

def cache_results(problem_id: str, user_code: str, language: str, results: List[TestResult]):
    """Cache Judge0 execution results"""
    cache_key = get_judge0_cache_key(problem_id, user_code, language)
    JUDGE0_CACHE[cache_key] = results
```

### Example 2: Updated analyze_code_submission with Caching
```python
# In src/backend/functions/tools.py
from src.utils.cache import get_cached_results, cache_results

def analyze_code_submission(
    problem_id: str,
    user_code: str,
    language: str = "python",
    user_id: str = "user_001"
) -> CodeAnalysisResponse:
    start_time = time.time()
    
    # Check cache first
    cached_results = get_cached_results(problem_id, user_code, language)
    if cached_results:
        print("✅ Cache HIT - returning cached test results")
        test_results = cached_results
        cache_hit = True
    else:
        print("❌ Cache MISS - executing tests")
        test_results = _run_mock_tests(problem_id, user_code)  # Will be Judge0 later
        cache_results(problem_id, user_code, language, test_results)
        cache_hit = False
    
    # Rest of function remains the same...
    all_passed = all(test.passed for test in test_results)
    detected_patterns = _detect_error_patterns(user_code, all_passed)
    
    # Log cache performance
    print(f"Cache hit: {cache_hit}, Execution time: {(time.time() - start_time)*1000:.2f}ms")
    
    return CodeAnalysisResponse(...)
```

---

## Appendix B: Monitoring & Alerting

### Cost Tracking Log Format
```python
# src/utils/cost_tracking.py
import json
from datetime import datetime

def log_api_call(
    endpoint: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
    latency_ms: float,
    cache_hit: bool
):
    """Log API call for cost tracking"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "endpoint": endpoint,
        "model": model,
        "tokens_input": input_tokens,
        "tokens_output": output_tokens,
        "cost_usd": cost_usd,
        "latency_ms": latency_ms,
        "cache_hit": cache_hit
    }
    
    with open("logs/api_costs.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### Daily Cost Summary Script
```python
# scripts/cost_summary.py
import json
from collections import defaultdict

def generate_daily_summary(log_file="logs/api_costs.jsonl"):
    """Generate daily cost summary from logs"""
    costs_by_endpoint = defaultdict(float)
    cache_hits = 0
    total_requests = 0
    
    with open(log_file, "r") as f:
        for line in f:
            entry = json.loads(line)
            costs_by_endpoint[entry["endpoint"]] += entry["cost_usd"]
            total_requests += 1
            if entry["cache_hit"]:
                cache_hits += 1
    
    print(f"Total requests: {total_requests}")
    print(f"Cache hit rate: {cache_hits/total_requests*100:.1f}%")
    print(f"Total cost: ${sum(costs_by_endpoint.values()):.2f}")
    for endpoint, cost in costs_by_endpoint.items():
        print(f"  {endpoint}: ${cost:.4f}")

if __name__ == "__main__":
    generate_daily_summary()
```

---

