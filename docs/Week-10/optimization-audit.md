# Optimization Audit

## 1. Current Costs

### Current Configuration
- **Model**: Gemini 2.0 Flash Exp
- **Average tokens per request**: ~500 tokens
- **Requests per user session**: 4 (initial chat + code analysis + follow-up + recommendation)
- **Current cost per request**: ~$0.01

### Monthly Usage Estimate (100 active users)
| Metric | Value |
|--------|-------|
| Users per month | 100 |
| Sessions per user | 10 |
| Requests per session | 4 |
| Total requests | 4,000 |
| **Current monthly cost** | **$40.00** |
| Avg response time | 2.5s |

### Cost Breakdown by Operation
- Code analysis: $0.012 (uses full context + AST parsing explanation)
- Problem recommendation: $0.008 (simple lookup + reasoning)
- Progress tracking: $0.010 (requires summarization)

---

## 2. Five Optimization Ideas

### Idea 1: Response Caching 
**What**: Cache identical requests (e.g., "What problem should I practice next?" with same weakness profile)
**Savings**: 30% fewer API calls (users often repeat queries)
**Implementation**: Simple dict cache with TTL (time-to-live of 5 minutes)

### Idea 2: Reduce Token Usage in Prompts 
**What**: Strip verbose problem descriptions and send only problem IDs to Gemini
**Savings**: ~40% token reduction per request
**Implementation**: Modify system prompt to be more concise

### Idea 3: Use Smaller Model for Simple Tasks 
**What**: Use Gemini 1.5 Flash for problem recommendations (read-only, low complexity)
**Savings**: 50% cost reduction on recommendations
**Implementation**: Dual-model routing based on task type

### Idea 4: Batch Analysis Requests
**What**: If user submits multiple attempts, analyze all at once instead of one-by-one
**Savings**: Reduces context-sending overhead by 60%
**Implementation**: Queue submissions and batch every 5 seconds

### Idea 5: Pre-compute Common Patterns
**What**: Generate AI feedback for common error patterns offline, serve from database
**Savings**: 80% reduction for repeat errors (e.g., "forgot to check for null")
**Implementation**: Store feedback templates, only call AI for unique errors

---

## 3. Top 3 Selected Ideas

We selected these based on **highest ROI** (savings vs implementation effort):

### 1. Response Caching (Idea 1)
**Why**: Easy to implement, immediate 30% savings, no quality loss
**Estimated savings**: $12/month

### 2. Reduce Token Usage (Idea 2)
**Why**: Low effort (rewrite prompts), 40% savings, improves speed
**Estimated savings**: $16/month

### 3. Dual Model Routing (Idea 3)
**Why**: Moderate effort, 50% savings on 25% of requests, maintains quality
**Estimated savings**: $5/month

**Total estimated savings**: **$33/month (82.5% reduction)**

---

## 4. Cost Savings Projection

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Monthly Cost** | $40.00 | $7.00 | -82.5% ↓ |
| **Cost per session** | $0.40 | $0.07 | -82.5% ↓ |
| **Avg response time** | 2.5s | 1.8s | -28% ↓ |
| **Cache hit rate** | 0% | 30% | +30% ↑ |
| **Tokens per request** | 500 | 300 | -40% ↓ |

### Breakdown by Optimization

| Optimization | Savings | % of Total Savings |
|--------------|---------|-------------------|
| Response Caching | $12/month | 36% |
| Token Reduction | $16/month | 48% |
| Dual Model Routing | $5/month | 15% |
| **Total** | **$33/month** | **82.5%** |

---

## 5. Implementation Plan

### Add Caching
- Implement TTL cache for identical requests
- Cache key: hash of (user_id + function_name + args)
- Expiry: 5 minutes

### Optimize Prompts
- Rewrite system prompts (remove verbose examples)
- Send problem IDs instead of full descriptions
- Test quality with 10 sample requests

### Dual Model Setup
- Add model routing logic: `if operation == "recommend" → use gemini-1.5-flash`
- Keep `gemini-2.0-flash-exp` for code analysis (needs intelligence)
- A/B test with 20% of users

### Measure & Validate
- Track actual costs vs projections
- Monitor user satisfaction (no quality drop)
- Adjust cache TTL if needed