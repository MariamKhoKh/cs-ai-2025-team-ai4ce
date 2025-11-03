---
# Architecture Explanation (v2)

## System Overview

The platform enables users to submit code, execute it in a sandboxed environment, and receive AI-generated feedback on performance and correctness. The system integrates FastAPI, PostgreSQL, and OpenAI APIs, with planned improvements for caching and monitoring.

```
await page.click('text=Two Sum');
  await page.fill('.monaco-editor', 'def two_sum(nums, target):\n    return []');
  await page.click('button:has-text("Submit")');
  
  // Wait for feedback
  await page.waitForSelector('.feedback-panel');
  const feedback = await page.textContent('.feedback-panel');
  expect(feedback).toContain('suboptimal_complexity');
});
```

---
## Component Overview

### 1. Frontend - React Application

**Technology Stack:**
- React 18.2
- Vite 4.5
- TypeScript 5.2
- Monaco Editor
- Recharts (visualization)

**Deployment:** Vercel (auto-deploy on main branch)

**Purpose:**
User interface for code submission, feedback display, and progress tracking.

**Key Responsibilities:**
- Render Monaco code editor for problem solving
- Display problem descriptions and test cases
- Submit code to backend API
- Show real-time execution results and feedback
- Visualize progress trends with line graphs
- Handle authentication with Clerk
- Client-side input validation

**Performance Target:** <1s page load (P95)

---

### 2. Backend - FastAPI Application

**Technology Stack:**
- FastAPI 0.104
- Python 3.11
- Pydantic v2
- SQLAlchemy (ORM)

**Deployment:** Railway (containerized, auto-deploy)

**Purpose:**
Core business logic, AI integration, and code analysis orchestration.

**Key Responsibilities:**
- API endpoint management (REST)
- JWT validation with Clerk
- Code execution orchestration (Judge0 API)
- AST parsing and analysis
- Error pattern classification (rule-based)
- GPT-4 explanation generation
- Database CRUD operations
- Recommendation algorithm
- Rate limiting (20 submissions/hour per user)

**API Endpoints:**

| Method | Endpoint | Purpose | Latency Target |
|--------|----------|---------|----------------|
| POST | `/api/problems/{id}/submit` | Submit code solution | <10s |
| GET | `/api/problems/recommended` | Get next problem | <500ms |
| GET | `/api/problems` | List all problems | <300ms |
| GET | `/api/progress` | User dashboard data | <500ms |

**Performance Target:** <10s total (submit to feedback)

---

### 3. Database - PostgreSQL

**Technology:** PostgreSQL 15 (Railway managed)

**Purpose:**
Persistent storage for user data, submissions, weakness profiles, and problems.

**Schema:**

**users table:**
```sql
- id (UUID, primary key)
- clerk_user_id (VARCHAR, unique)
- email (VARCHAR)
- created_at (TIMESTAMP)
- total_problems_solved (INT)
```

**problems table:**
```sql
- id (UUID, primary key)
- title (VARCHAR)
- description (TEXT)
- difficulty (VARCHAR: Easy/Medium/Hard)
- optimal_time_complexity (VARCHAR)
- test_cases (JSONB)
- tags (TEXT[])
```

**submissions table:**
```sql
- id (UUID, primary key)
- user_id (UUID, foreign key)
- problem_id (UUID, foreign key)
- code (TEXT)
- passed (BOOLEAN)
- execution_time_ms (INT)
- test_results (JSONB)
- created_at (TIMESTAMP)
```

**weakness_patterns table:**
```sql
- id (UUID, primary key)
- user_id (UUID, foreign key)
- pattern_type (VARCHAR)
- frequency (INT)
- last_occurred (TIMESTAMP)
- mastery_score (FLOAT 0-100)
```

**Key Indexes:**
- `idx_users_clerk_id` on users(clerk_user_id)
- `idx_submissions_user` on submissions(user_id)
- `idx_submissions_created` on submissions(created_at DESC)
- `idx_patterns_user` on weakness_patterns(user_id)
- GIN index on problems(tags)

**Performance Target:** <100ms query time

---

### 4. Code Execution - Judge0 API

**Service:** Judge0 Cloud API (https://judge0.com)

**Configuration:**
- Language: Python 3.11
- Time Limit: 5 seconds
- Memory Limit: 128 MB
- CPU Time Limit: 2 seconds
- Network Access: Disabled (security)

**Purpose:**
Sandboxed code execution with security isolation and resource limits.

**Security Features:**
- Isolated Docker containers
- No file system access
- No network access
- Auto-kill infinite loops (timeout)
- Limited memory prevents memory bombs

**Fallback Strategy:**
1. Primary: Judge0 API
2. Retry Judge0 (3 attempts with exponential backoff)
3. Fallback: Piston API (alternative service)
4. Ultimate: Return error, allow user retry

**Performance Target:** <6s execution time

---

### 5. AI Services - OpenAI GPT-4

**Models:**
- **Primary:** GPT-4o-mini (80% of queries)
- **Complex cases:** GPT-4o (20% of queries)

**Configuration:**
- Max Tokens: 500
- Temperature: 0.3 (consistent responses)
- Top P: 1.0
- Frequency Penalty: 0.2

**Purpose:**
Generate natural language explanations of coding mistakes.

**Model Selection Logic:**
```python
simple_patterns = [
    'missing_edge_case_null',
    'off_by_one_error',
    'missing_input_validation'
]

if pattern in simple_patterns:
    use gpt-4o-mini  # $0.00015/1K tokens
else:
    use gpt-4o       # $0.0025/1K tokens
```

**Caching Strategy (Planned Week 6):**
- Cache identical pattern + problem combinations for 24 hours
- Expected 40% cache hit rate
- Redis for caching layer

**Cost Control:**
- Average: ~$0.015 per query
- Monthly budget (1000 queries): ~$15
- With caching: ~$9

**Fallback Strategy:**
1. Primary: OpenAI API
2. If down: Return generic explanation based on pattern
3. If rate limited: Queue for retry in 1 minute
4. If error persists: Show error to user

**Performance Target:** <3s response time

---

### 6. Authentication - Clerk

**Service:** Clerk (https://clerk.com)  
**Plan:** Free tier (10,000 monthly active users)

**Purpose:**
User authentication and JWT token management.

**Supported Auth Methods:**
- Email + password
- OAuth (Google)
- Magic links (passwordless)

**JWT Structure:**
```json
{
  "sub": "user_2abc123",
  "email": "student@university.edu",
  "exp": 1698451200,
  "iat": 1698447600
}
```

**Security Features:**
- JWTs expire after 1 hour
- Automatic refresh token management
- No sensitive data in JWT payload
- Backend validates signature using Clerk's public key
- HTTPS only (enforced)

**Performance:** Negligible latency (<50ms validation)

---

### 7. Pattern Detection - Rule-Based Classifier

**Technology:** Python AST module + custom rules

**Purpose:**
Classify code mistakes into 6 error categories.

**6 Error Patterns Detected:**

1. **missing_edge_case_null:** No check for None, empty array, single element
2. **suboptimal_complexity:** O(n²) when O(n) or O(n log n) possible
3. **wrong_data_structure:** Using list when set/dict is better
4. **off_by_one:** Incorrect range/loop boundaries
5. **missing_input_validation:** No checks for problem constraints
6. **inefficient_nested_loops:** Nested loops when single pass possible

**Detection Approach:**
- Parse code into Abstract Syntax Tree (AST)
- Extract features (loop depth, conditionals, data structures)
- Apply rule-based classification
- Cross-reference with problem requirements

**Performance Target:** <300ms analysis time

---

## Technology Choices & Justifications

### FastAPI vs Flask

**Chose:** FastAPI

**Pros:**
- Async/await support (needed for concurrent Judge0 + OpenAI calls)
- Automatic API documentation (Swagger at /docs)
- Type safety with Pydantic (catches bugs early)
- Fast performance (comparable to Node.js)

**Cons:**
- Smaller community than Flask
- Steeper learning curve (async programming)

**Tradeoff Accepted:** Learning curve worth it for async support and type safety.

---

### PostgreSQL vs MongoDB

**Chose:** PostgreSQL

**Pros:**
- Strong ACID guarantees (data integrity)
- Relational structure fits our data model (users → submissions → patterns)
- Complex queries easy with SQL
- Foreign keys enforce referential integrity
- Free tier on Railway includes Postgres

**Cons:**
- Less flexible schema
- Migrations required when schema changes

**Tradeoff Accepted:** Stricter schema worth it for data integrity and relational queries.

---

### Clerk vs DIY Auth

**Chose:** Clerk

**Pros:**
- Production-ready out of box (OAuth, password resets, email verification)
- Beautiful pre-built UI components
- Free tier generous (10K users)
- Excellent React integration
- Automatic JWT generation and validation

**Cons:**
- Vendor lock-in (switching later difficult)
- Less control over auth flow
- Dependency on third-party service

**Tradeoff Accepted:** Vendor lock-in acceptable to save 2-3 weeks development time. Building secure auth from scratch is complex and error-prone.

---

### GPT-4o-mini vs GPT-4o

**Chose:** Hybrid (80% mini, 20% full)

**Pros:**
- 90% cost savings vs GPT-4o only ($4.50/month vs $45/month)
- Quality nearly identical for simple patterns
- Flexibility to use full model when needed

**Cons:**
- More complex routing logic
- Two API integrations to maintain

**Tradeoff Accepted:** Added complexity worth it for massive cost savings. Without this optimization, would exceed semester budget by 9x.

---

### Judge0 Cloud vs Self-Hosted

**Chose:** Judge0 Cloud API (for MVP)

**Pros:**
- No infrastructure setup (just API calls)
- Proven security (used by LeetCode, HackerRank)
- Reliable sandbox (Docker containers)
- Free tier sufficient for testing

**Cons:**
- Costs money at scale ($0.002/execution)
- Dependent on third-party service
- Occasional slowness (6s for complex code)

**Tradeoff Accepted:** Dependency and cost acceptable for faster MVP launch. Self-hosting would take 1-2 weeks to set up securely.

**Future Plan:** If we scale beyond 100 users/day, self-host Judge0 on Railway.

---

### Rule-Based vs Machine Learning

**Chose:** Rule-based (for MVP)

**Pros:**
- No training data required (can launch immediately)
- Interpretable (easy to debug)
- Fast inference (<100ms)
- Easy to iterate (just update rules)

**Cons:**
- Lower accuracy (70-75% vs 85-90% for ML)
- Brittle (breaks on edge cases)
- Requires manual rule engineering

**Tradeoff Accepted:** Lower accuracy acceptable to launch faster. Don't have time to collect and label 500+ training examples.

**Future Plan:** After collecting 200+ labeled submissions (Week 8-15), train Random Forest model (Week 16+, post-course).

---

## Data Flow: Code Submission Pipeline

**Step-by-Step Process:**

1. **User writes code** in Monaco editor (Frontend)
2. **User clicks Submit** → Frontend sends POST /submit
3. **Backend receives request** → Validates JWT
4. **Judge0 execution** → Runs code against test cases (3-6s)
5. **If tests fail:**
   - Parse code into AST (200ms)
   - Detect error patterns (300ms)
   - Call GPT-4 for explanation (2-3s)
6. **Update database** → Store submission, update weakness profile (100ms)
7. **Return response** → Frontend displays results + feedback

**Total Latency:** 6-10 seconds

**Latency Breakdown (P95):**
- Judge0 execution: 6s
- GPT-4 explanation: 3s
- Other processing: 500ms
- **Total: ~9.5s** (within 10s target)

---

## Security Architecture

### Security Boundaries

**Layer 1: Frontend**
- ✅ HTTPS enforced (Vercel)
- ✅ Content Security Policy (CSP) headers
- ✅ JWT stored in memory (not localStorage)
- ✅ Input validation (max 5000 chars, syntax check)

**Layer 2: Backend API**
- ✅ JWT validation on all protected endpoints
- ✅ Rate limiting (20 submissions/hour per user)
- ✅ CORS (only frontend domain allowed)
- ✅ Input sanitization

**Layer 3: Database**
- ✅ Encrypted at rest (Railway default)
- ✅ Encrypted in transit (SSL)
- ✅ Limited access (firewall rules)
- ✅ Parameterized queries (SQLAlchemy ORM)

**Layer 4: Code Execution**
- ✅ Sandboxed containers (Judge0)
- ✅ No network access
- ✅ No file system access
- ✅ Resource limits (5s timeout, 128MB memory)

---

### Failure Points & Mitigation

**Failure 1: Judge0 API Down**
- **Impact:** Cannot execute user code
- **Mitigation:** 
  - Retry 3 times with exponential backoff
  - Fallback to Piston API
  - Show error message to user
- **User Experience:** "Code execution service temporarily unavailable. Please try again in a few minutes."

**Failure 2: OpenAI API Down**
- **Impact:** Cannot generate explanations
- **Mitigation:**
  - Retry 3 times
  - Return generic explanation based on pattern type
  - Still show test results
- **User Experience:** Pattern detected, generic hint provided instead of AI explanation

**Failure 3: Database Connection Lost**
- **Impact:** Cannot store submissions or retrieve user data
- **Mitigation:**
  - Connection pooling with auto-reconnect
  - Circuit breaker pattern (stop trying after 5 failures)
  - Queue submissions for later storage
- **User Experience:** "We're experiencing technical difficulties. Your submission will be saved when service resumes."

**Failure 4: Clerk Authentication Down**
- **Impact:** Users cannot log in (CRITICAL)
- **Mitigation:** None (hard dependency)
- **User Experience:** "Authentication service unavailable. Please try again later."
- **Risk Acceptance:** Acceptable for MVP. In production, would implement fallback auth.

**Failure 5: Frontend CDN Issues**
- **Impact:** Users cannot access site
- **Mitigation:** Vercel's global CDN provides automatic failover
- **User Experience:** Minimal impact (CDN highly reliable)

---

## Changes Since Week 2

### Component Changes

| Component | Week 2 Plan | Week 4 Reality | Reason |
|-----------|-------------|----------------|---------|
| **Backend Framework** | Flask | FastAPI | Needed async for concurrent API calls |
| **Database** | MongoDB | PostgreSQL | Relational structure better for our data model |
| **AI Model** | GPT-4 only | GPT-4o-mini (80%) + GPT-4o (20%) | Cost: 90% savings without quality loss |
| **ML Approach** | Random Forest | Rule-based | No time to collect/label 500 examples |
| **Code Execution** | Uncertain | Judge0 API | Tested both Judge0/Piston, Judge0 more reliable |
| **Caching** | None | Redis (Week 6) | Discovered repeated queries common |
| **Deployment** | Heroku | Railway | Better free tier, Postgres included |
| **Auth** | Firebase | Clerk | Better React integration, more generous free tier |

### Why Changes Were Made

**1. Flask → FastAPI**
- **Trigger:** Realized we need to call Judge0 (6s) and OpenAI (3s). Sequential = 9s, too slow.
- **Solution:** FastAPI's async/await allows concurrent calls where possible.
- **Impact:** Better architecture for future optimizations.

**2. MongoDB → PostgreSQL**
- **Trigger:** Week 3 data modeling session revealed strong relationships (users→submissions→patterns).
- **Solution:** PostgreSQL foreign keys enforce data integrity.
- **Impact:** Prevents orphaned records, enables complex JOINs.

**3. GPT-4 only → Hybrid model**
- **Trigger:** Week 3 cost projection showed $45/month (90% over budget).
- **Solution:** Use cheaper GPT-4o-mini for simple patterns (tested accuracy: 85% vs 90%).
- **Impact:** $4.50/month cost, within budget.

**4. Random Forest → Rule-based**
- **Trigger:** Realized we don't have training data and can't collect 500 examples in time.
- **Solution:** Build rule-based classifier (can launch Week 5).
- **Impact:** 70% accuracy vs 85%, but we can launch 3 weeks earlier.

**5. Heroku → Railway**
- **Trigger:** Heroku removed free tier.
- **Solution:** Railway offers free credits + Postgres included.
- **Impact:** $0 vs $7/month on Heroku.

### Diagram Changes Visualization

**🟢 Green = Added components**
- Redis caching layer (Week 6)
- Rate limiting middleware
- Hybrid GPT-4 routing logic

**🟡 Yellow = Modified components**
- FastAPI replaces Flask
- PostgreSQL replaces MongoDB
- Railway replaces Heroku

**🔴 Red = Removed components**
- ~~MongoDB~~
- ~~Random Forest model~~
- ~~Heroku dynos~~

---

## Potential Bottlenecks

### Identified Bottlenecks

**1. Judge0 Execution Time (6s)**
- **Current:** 6s worst case for complex algorithms
- **Impact:** 60% of total latency
- **Mitigation:** 
  - Upgrade to paid tier for priority queue (planned Week 6)
  - Consider self-hosting for <500ms improvement
- **Risk:** HIGH (directly impacts user experience)

**2. GPT-4 Response Time (3s)**
- **Current:** 3s worst case
- **Impact:** 30% of total latency
- **Mitigation:**
  - Reduce prompt tokens 500→250 (saves 1-1.5s)
  - Cache responses (40% hit rate expected)
- **Risk:** MEDIUM (optimizations planned Week 5-6)

**3. Database Query Time (<100ms)**
- **Current:** 80ms average, 150ms P95
- **Impact:** Minimal for single queries, problematic if N+1 queries
- **Mitigation:**
  - Indexes on frequently queried columns (done)
  - Eager loading for relationships (SQLAlchemy)
  - Monitor slow queries with pg_stat_statements
- **Risk:** LOW (well under target)

**4. Judge0 Free Tier Rate Limit (60/day)**
- **Current:** 60 executions/day free
- **Impact:** With 20 users × 5 problems/day = 100 needed
- **Mitigation:** Upgrade to paid tier ($0.002/execution = $6/month)
- **Risk:** MEDIUM (must upgrade by Week 6)

**5. OpenAI API Costs**
- **Current:** $0.015/query × 500/month = $7.50
- **Impact:** Within budget but no room for growth
- **Mitigation:** Caching reduces to $4.50/month
- **Risk:** LOW (caching planned Week 6)

### Performance Optimization Plan

**Week 5:**
- [ ] Reduce GPT-4 prompt tokens (500→250)
- [ ] Pre-compile AST parser regex patterns
- **Expected improvement:** -1.5s total latency

**Week 6:**
- [ ] Implement Redis caching for GPT responses
- [ ] Upgrade Judge0 to paid tier
- **Expected improvement:** -2s total latency (from cache hits)

**Week 7:**
- [ ] Add database query monitoring
- [ ] Optimize N+1 queries with eager loading
- **Expected improvement:** -50ms database time

**Target:** <10s total latency by Week 6 (currently ~12s)

---

## Cost Analysis

### Monthly Cost Breakdown

**Assumptions:**
- 30 active users during course
- Each user solves 10 problems/month
- Total: 300 submissions/month

| Service | Free Tier | Usage | Cost |
|---------|-----------|-------|------|
| Vercel (Frontend) | ✅ Unlimited | 50 deploys/month | $0 |
| Railway (Backend + DB) | ✅ $5 credit | ~$3/month | $0 |
| Judge0 API | ❌ 60/day | 300 executions | $0.60 |
| OpenAI API | ❌ Pay-per-use | 300 queries | $4.50 |
| Clerk (Auth) | ✅ 10K users | 30 users | $0 |
| **TOTAL** | | | **$5.10/month** |

**Semester Total (11 weeks):**
- $5/month × 2.75 months = $13.75
- Buffer: +$10
- **Expected: $23.75 of $50 budget** ✅

**With Caching (Week 6+):**
- 40% cache hit rate
- OpenAI: $4.50 × 0.6 = $2.70
- **New total: $3.30/month**
- **Semester: $9.08** ✅

---

## Latency Budget Annotations

### Performance Targets by Component

| Component | Target (P95) | Current | Status |
|-----------|--------------|---------|--------|
| Frontend page load | <1s | 850ms | ✅ |
| Code submission (total) | <10s | ~12s | ⚠️ |
| Judge0 execution | <6s | ~6s | ⚠️ |
| AST parsing | <500ms | 200ms | ✅ |
| Pattern detection | <500ms | 300ms | ✅ |
| GPT-4 explanation | <3s | ~4s | ⚠️ |
| Database write | <100ms | 80ms | ✅ |
| Problem recommendation | <500ms | 400ms | ✅ |

**Overall Target:** <10 seconds from submit to feedback  
**Current Performance:** ~12 seconds  
**Gap to Close:** 2 seconds (achievable with planned optimizations)

---

## Architecture Review Status

**Completed:**
- [x] All components documented
- [x] Technology choices justified
- [x] Tradeoffs documented
- [x] Security boundaries defined
- [x] Failure points identified
- [x] Performance targets set
- [x] Cost analysis completed
- [x] Changes from Week 2 highlighted
- [x] Bottlenecks identified

**Remaining:**
- [ ] Team review and approval
- [ ] Diagram visual update with color coding
- [ ] Final proofread

---

**Version:** 2.0  
**Last Updated:** October 25, 2025 (Week 4)  
**Contributors:** Backend Lead, Frontend Lead, ML Lead
---
    await expect(page.locator('text=All tests passed').first()).toBeVisible({ timeout: 10000 });
});
```
