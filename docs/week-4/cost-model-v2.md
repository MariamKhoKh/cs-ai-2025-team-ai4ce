# Token Usage & Cost Model (Version 2)

**Project:** CodeMentor AI  
**Team:** AI4ce  
**Date:** Week 4, October 26, 2025  
**Version:** 2.0

---

## Executive Summary

- **Current Cost Per Query:** $0.042
- **Projected Monthly Cost (Production):** $84
- **Optimization Potential:** 71% cost reduction identified
- **Budget Status:**  On track

**Key Insight:** GPT-4 explanations account for 85% of costs. Switching to GPT-4o-mini for initial explanations with GPT-4o escalation can reduce costs by 65% while maintaining quality.

---

## 1. Current Baseline (Week 4)

### Token Usage Breakdown
Based on actual usage from Week 3-4 testing:

| Component | Tokens | Cost (GPT-4o) | % of Total |
|:----------|-------:|-------------:|-----------:|
| **Code Analysis Request** | | | |
| System prompt | 350 | $0.00175 | 4% |
| User code | 400 | $0.00200 | 5% |
| Problem description | 250 | $0.00125 | 3% |
| Test results | 200 | $0.00100 | 2% |
| **Input Subtotal** | **1,200** | **$0.00600** | **14%** |
| **Output (Explanation)** | **2,400** | **$0.03600** | **86%** |
| **TOTAL PER QUERY** | **3,600** | **$0.04200** | **100%** |

### Current Usage Patterns

**Week 3-4 Testing Data:**
- Total queries: 47 problem attempts
- Average queries/day: 6 queries
- Total tokens used: 169,200 tokens
- Total cost incurred: $1.97
- Model used: GPT-4o

---

## 2. Cost Model (Current vs. Projected)

### Development Phase (Weeks 3-9)
- Queries per day: ~10-15 (team testing)
- Days remaining: 42 days
- Estimated queries: 420-630 queries
- **Projected cost:** $17.64 - $26.46

### Production Phase (Weeks 10-15)
- Queries per day: 60-100 (8 users × 8-12 problems each)
- Days: 42 days
- Estimated queries: 2,520-4,200 queries
- **Projected cost:** $105.84 - $176.40

### Total Semester Projection

| Phase | Queries | Cost (Current) | Cost (Optimized) | Savings |
|:------|--------:|---------------:|-----------------:|--------:|
| Development (W3-9) | 420-630 | $18-$26 | $5-$8 | 71% |
| Production (W10-15) | 2,520-4,200 | $106-$176 | $31-$51 | 71% |
| **TOTAL** | **2,940-4,830** | **$124-$202** | **$36-$59** | **71%** |

 **Current model exceeds $200 budget**

---

## 3. Optimization Strategies

### Strategy 1: Hybrid Model Selection  **CRITICAL**

**Problem:** GPT-4o explanations cost $0.036 per query (86% of total cost)

**Solution:** Use GPT-4o-mini first, escalate to GPT-4o only if needed

**Implementation:**
```python
def generate_explanation(code, error_type, complexity="medium"):
    # 90% of cases: Use mini
    if complexity in ["easy", "medium"]:
        model = "gpt-4o-mini"  # $0.0015/query output
    else:  # Complex patterns, unclear errors
        model = "gpt-4o"       # $0.0360/query output
    
    return call_openai(model=model, prompt=build_prompt(...))
```

**Expected Distribution:** 90% mini, 10% full

**Cost Calculation:**
- Mini: 2,400 tokens × $0.0006/1K = $0.00144/query
- Blended: (0.90 × $0.00144) + (0.10 × $0.03600) = $0.00490/query
- **Total per query:** $0.006 (input) + $0.00490 (output) = **$0.01090**
- **Savings:** 74% reduction → **$88/semester saved**

**Implementation effort:** 2 hours  
**Priority:** Week 5 (MUST DO)

---

### Strategy 2: Compress System Prompt

**Current (350 tokens):**
```
You are an expert programming tutor analyzing code submissions for 
technical interview preparation. Your role is to identify patterns 
in errors and provide educational feedback. Be encouraging but 
honest about mistakes. Focus on conceptual understanding, not just 
correctness. Explain time complexity clearly. Consider edge cases...
```

**Optimized (150 tokens - 57% reduction):**
```
Analyze code for interview prep. Identify error patterns (edge cases, 
complexity, data structures). Provide educational feedback on concepts, 
not just correctness. Be concise.
```

**Token Savings:** 200 tokens input  
**Cost Savings:** $0.001/query → **$3.43/semester** (3%)  
**Implementation effort:** 30 minutes  
**Priority:** Week 4 (Quick win)

---

### Strategy 3: Structured Output for Code Analysis

**Current Output (2,400 tokens):**
```json
{
  "analysis": "Your code has a time complexity issue. The nested loops 
              create O(n²) behavior when this problem can be solved in 
              O(n) using a hash map. Here's why this matters: in 
              interviews, complexity is critical...",
  "error_types": ["suboptimal_complexity"],
  "explanation": "Let me explain the optimal approach..."
}
```

**Optimized with Schema (1,200 tokens - 50% reduction):**
```json
{
  "error_types": ["suboptimal_complexity"],
  "time_complexity": "O(n²)",
  "optimal_complexity": "O(n)",
  "concept": "hash_map_optimization",
  "explanation": "Nested loops → O(n²). Use hash map → O(n)."
}
```

**Token Savings:** 1,200 tokens output  
**Cost Savings:** Reduces mini output by 50% → **$0.00072/query saved**  
**Combined with Strategy 1:** $0.01018/query total  
**Semester savings:** Additional **$2.47** (2%)  
**Implementation effort:** 3 hours  
**Priority:** Week 6

---

### Strategy 4: Cache Problem Descriptions

**Problem:** Same problem description sent with every attempt (250 tokens)

**Solution:** 
```python
# Cache in Redis
problem_cache = {
    "two-sum": {
        "description": "...",
        "constraints": "...",
        "tokens": 250
    }
}

# Send only problem_id in API call
def analyze_code(problem_id, code):
    # Retrieve from cache, don't send full description
    problem = redis.get(f"problem:{problem_id}")
```

**Expected savings:** 250 tokens × 50% reuse rate  
**Cost Savings:** $0.000625/query → **$2.15/semester** (2%)  
**Implementation effort:** 2 hours  
**Priority:** Week 7 (Nice to have)

---

### Strategy 5: AST Analysis Before LLM

**Concept:** Detect simple errors (syntax, missing base case) without calling GPT

```python
def analyze_submission(code):
    # Free AST analysis first
    ast_errors = parse_ast(code)
    
    if ast_errors in ["syntax_error", "missing_return"]:
        # Rule-based response (no API call)
        return generate_template_feedback(ast_errors)
    
    # Only call LLM for complex pattern detection
    return call_openai_analysis(code)
```

**Expected reduction:** 15% of queries avoided  
**Cost Savings:** 15% × $0.01018 = $0.00153/query → **$5.25/semester** (4%)  
**Implementation effort:** 4 hours  
**Priority:** Week 8 (If time permits)

---

## 4. Combined Optimization Impact

### Phased Rollout

| Week | Optimization | Effort | Cost/Query | Cumulative Savings |
|:-----|:-------------|-------:|-----------:|-------------------:|
| **Baseline** | - | - | $0.04200 | - |
| **Week 4** | Compress prompt | 30 min | $0.04100 | 2% |
| **Week 5** | Hybrid model  | 2 hrs | $0.01090 | 74% |
| **Week 6** | Structured output | 3 hrs | $0.01018 | 76% |
| **Week 7** | Cache problems | 2 hrs | $0.00956 | 77% |
| **Week 8** | AST pre-filter | 4 hrs | $0.00812 | 81% |

### Final Projections

**Optimized Costs:**
- Development (W3-9): 525 queries × $0.00812 = **$4.26**
- Production (W10-15): 3,360 queries × $0.00812 = **$27.28**
- **Total semester: $31.54** (within budget by $168!)

---

## 5. Implementation Roadmap

###  Week 4 (This Week - 45 min)
- [ ] Compress system prompt (30 min)
- [ ] Set up cost tracking spreadsheet (15 min)
- **Expected savings:** $3.43

###  Week 5 (CRITICAL - 2 hours)
- [ ] Implement GPT-4o-mini/GPT-4o hybrid (2 hours)
- [ ] Test quality on 20 examples
- [ ] Measure cost reduction
- **Expected savings:** $88.31 ← **PRIORITY**

### Week 6 (3 hours)
- [ ] Add Pydantic models for structured output
- [ ] Update API call with JSON schema
- [ ] Validate with 10 problems
- **Expected savings:** $2.47

### Week 7 (Optional - 2 hours)
- [ ] Set up Redis for problem caching
- [ ] Implement cache-aside pattern
- **Expected savings:** $2.15

### Week 8 (Optional - 4 hours)
- [ ] Add AST pre-filtering
- [ ] Create rule-based templates
- **Expected savings:** $5.25

---

## 6. Budget Allocation

| Category | Budgeted | Projected | Status |
|:---------|----------:|----------:|:-------|
| **AI API (Optimized)** | $40 | $31.54 |  Under |
| **User Testing Incentives** | $80 | $80 | On track |
| **Infrastructure** | | | |
| - Railway (Backend+DB) | $10 | $10 | On track |
| - Judge0 (Code execution) | $20 | $20 | On track |
| - Redis (Cache) | $5 | $0 | Free tier |
| **Buffer/Contingency** | $45 | $45 | Reserved |
| **TOTAL** | **$200** | **$186.54** |  **Healthy** |

---

## 7. Cost Alerts & Monitoring

### Alert Thresholds
-  **Warning:** Daily spend >$2 (>20 queries/day in dev)
-  **Critical:** Weekly spend >$10 (indicates overuse)

### Tracking Metrics
- Daily: Cost per query (target: <$0.012)
- Weekly: Total spend vs. projection
- Model distribution: % GPT-4o-mini vs GPT-4o (target: 90/10)

### Dashboard (Google Sheet)
```
Date       | Queries | Model Mix      | Cost   | Notes
-----------|---------|----------------|--------|----------------
Oct 26     | 8       | 100% GPT-4o    | $0.34  | Baseline
Nov 2      | 12      | 90% mini       | $0.13  | After optimization
```

---

## 8. Alternative Models Considered

| Model | Input | Output | Quality | Decision |
|:------|------:|-------:|:--------|:---------|
| GPT-4o | $0.005/1K | $0.015/1K | Excellent | Use for 10% |
| GPT-4o-mini | $0.00015/1K | $0.0006/1K | Very good | Use for 90%  |
| Claude Sonnet | $0.003/1K | $0.015/1K | Excellent | Not needed |
| Llama 3.1 (self-hosted) | ~$0.0001/1K | ~$0.0001/1K | Good | Too much infra work |

**Decision:** Stick with OpenAI hybrid approach for simplicity and quality.

---

## Cost Optimization Checklist

**This Week (Week 4):**
- [ ] Compress system prompt
- [ ] Document baseline metrics
- [ ] Set up tracking sheet

**Next Week (Week 5) - CRITICAL:**
- [ ] Implement hybrid model selection
- [ ] A/B test 20 explanations (compare quality)
- [ ] Validate 74% cost reduction

**Weeks 6-8 (If time permits):**
- [ ] Structured output
- [ ] Problem caching
- [ ] AST pre-filtering

---

**Document Version:** 2.0  
**Last Updated:** October 26, 2025  
**Next Review:** Week 6 (after hybrid model implementation)