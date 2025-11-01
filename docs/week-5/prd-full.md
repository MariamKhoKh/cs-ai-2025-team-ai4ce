# CodeMentor AI - Project Overview Document
---

## 1. Project Goal & Core Problem

**Goal:** Enable candidates preparing for technical interviews to identify and overcome their systematic coding weaknesses through AI-powered pattern detection and personalized feedback.

**Core Problem:** Candidates solve 50-100 LeetCode problems but keep making the same mistakes (e.g., always choosing O(n²) solutions, missing edge cases for empty arrays) because existing platforms only show "Accepted" or "Wrong Answer" without analyzing *why* their approach is suboptimal. They waste time on random problems instead of targeting their actual gaps, and with only 2-3 interview attempts before 6-12 month waiting periods, inefficient practice is costly.

---

## 2. MVP Scope & Key Features

### Features IN Scope for MVP (Week 15 Demo)

**Core Features (Must Have - P1):**

1. **Code Execution Sandbox** - Submit code and execute against test cases in isolated environment (Judge0 API)
2. **Error Pattern Detection** - Classify 6 error types: missing edge cases, suboptimal complexity, wrong data structure, off-by-one errors, missing validation, inefficient loops
3. **GPT-4 Explanations** - Generate natural language feedback explaining mistakes and how to improve
4. **User Weakness Profile** - Track recurring error patterns per user across all submissions
5. **Pattern Frequency Tracking** - Count how often each error type occurs, show percentage breakdown
6. **Progress Dashboard** - Visual dashboard with weakness trend charts, solved problems count, mastery scores
7. **Personalized Problem Queue** - Recommend next problems based on detected weaknesses (70%+ helpfulness target)
8. **Complexity Feedback** - Detect time complexity from code and suggest when better complexity exists
9. **Edge Case Detection** - Identify missed null/empty/boundary checks and point to specific failures
10. **AST Code Analysis** - Parse Python code structure to extract features (loops, conditionals, complexity)
11. **Test Case Runner** - Execute code against all test cases, show pass/fail with expected vs actual output
12. **Problem Database** - 30 curated interview problems (15 arrays, 8 strings, 7 hash maps) with edge cases

### Features OUT of Scope for MVP

**Deferred to Post-Course (Phase 2-4):**

- Multi-language support (JavaScript, Java, C++) - Python only for MVP
- Adaptive difficulty adjustment based on success rate
- Interview readiness score prediction
- Spaced repetition scheduling for weak areas
- Video explanations of solutions
- Interactive debugging/step-through
- System design interview prep
- Behavioral interview questions
- Live mock interviews with AI
- Company-specific problem sets
- Collaborative coding (pair programming mode)
- Mobile applications (web-first approach)
- Social features (leaderboards, peer comparison)
- Custom problem upload by users

---

## 3. Target Audience

**Primary User: CS Students Preparing for FAANG Interviews**

**Demographics:**
- Age: 20-22 years old
- Education: CS major (junior/senior level) or bootcamp graduates
- Experience: Completed Data Structures & Algorithms coursework, moderate coding proficiency
- Timeline: Preparing 1-2 hours daily for 8-12 weeks before interview season

**User Context:**
- Applying for summer internships or new grad positions at FAANG companies
- Have practiced on LeetCode but lack clarity on improvement areas
- Experience time pressure in interviews despite knowing solutions
- Need measurable progress tracking to gauge readiness

**Key Pain Points:**
- "I solve problems but don't know if I'm actually improving"
- "LeetCode doesn't tell me why my approach is wrong, just that it is"
- "I run out of time even when I know the solution"
- "I keep making the same mistakes but don't realize it"

---

## 4. Technology Stack (Specific Versions)

| Category | Technology | Specific Version | Notes |
|----------|-----------|------------------|-------|
| **Language (Backend)** | [Python / JavaScript] | [TBD - To be filled in] | Primary backend language |
| **Language (Frontend)** | [Python / JavaScript] | [TBD - To be filled in] | Primary frontend language |
| **Backend Framework** | FastAPI | 0.104.0 | Async support for concurrent API calls |
| **Frontend Framework** | React | 18.2.0 | With TypeScript 5.2 |
| **Build Tool** | Vite | 4.5.0 | Fast dev server and builds |
| **Code Editor** | Monaco Editor | @monaco-editor/react 4.6.0 | VS Code's editor component |
| **UI Component Library** | Recharts | 2.9.0 | For progress visualization |
| **Database** | PostgreSQL | 15.3 | Hosted on Railway |
| **Cache Layer** | Redis | 7.2.0 | Problem recommendations, caching |
| **ORM** | SQLAlchemy | 2.0.23 | For database operations |
| **Authentication** | Clerk | Latest | JWT-based auth |
| **Code Execution** | Judge0 API | Cloud API | Sandboxed code execution |
| **AI Model (Primary)** | GPT-4o-mini | Latest | 90% of queries ($0.00144/query) |
| **AI Model (Complex)** | GPT-4o | Latest | 10% of queries ($0.036/query) |
| **Testing (Backend)** | pytest | 7.4.0 | Unit and integration tests |
| **Testing (Frontend)** | Jest | 29.6.2 | Unit tests |
| **Testing (E2E)** | Playwright | 1.40.0 | Browser automation |
| **Load Testing** | k6 | 0.47.0 | Performance testing |
| **Monitoring** | Sentry | Latest | Error tracking (free tier) |
| **Deployment (Frontend)** | Vercel | N/A | Auto-deploy on main branch |
| **Deployment (Backend)** | Railway | N/A | Containerized, auto-deploy |
| **Version Control** | Git | N/A | Repo on GitHub |
| **CI/CD** | GitHub Actions | N/A | Automated testing on PR |

---

## 5. High-Level Architecture

### Architecture Style

Hybrid monolith-plus-API architecture with external AI and execution services:
- **Frontend:** React SPA hosted on Vercel
- **Backend:** FastAPI monolith on Railway
- **External Services:** Judge0 (execution), OpenAI (explanations), Clerk (auth)
- **Data Layer:** PostgreSQL (persistent storage) + Redis (caching)

### Mermaid Architecture Diagram

```mermaid
graph TB
    User[User Browser]
    FE[Frontend React App<br/>Vercel]
    BE[Backend FastAPI<br/>Railway]
    DB[(PostgreSQL<br/>Railway)]
    Cache[(Redis<br/>Railway)]
    Judge0[Judge0 API<br/>Code Execution]
    OpenAI[OpenAI API<br/>GPT-4o/mini]
    Clerk[Clerk Auth<br/>JWT Provider]
    
    User -->|HTTPS| FE
    FE -->|API Calls| BE
    FE -->|Auth| Clerk
    BE -->|Validate JWT| Clerk
    BE -->|Store/Query| DB
    BE -->|Cache| Cache
    BE -->|Execute Code| Judge0
    BE -->|Generate Feedback| OpenAI
    
    subgraph Analysis Pipeline
        BE -->|1. Submit| Judge0
        Judge0 -->|2. Results| BE
        BE -->|3. Parse AST| BE
        BE -->|4. Detect Patterns| BE
        BE -->|5. Explain| OpenAI
        OpenAI -->|6. Feedback| BE
        BE -->|7. Store| DB
    end
    
    style FE fill:#e1f5ff
    style BE fill:#fff4e1
    style DB fill:#f0f0f0
    style Cache fill:#f0f0f0
    style Judge0 fill:#ffe1e1
    style OpenAI fill:#ffe1e1
    style Clerk fill:#ffe1e1
```

---

## 6. Core Components/Modules

### Frontend Components

1. **ProblemList** - Browse and filter 30 interview problems by difficulty/tags
2. **ProblemDetail** - Display problem description, examples, constraints, starter code
3. **CodeEditor** - Monaco editor with syntax highlighting, auto-complete, theme toggle
4. **TestResults** - Show pass/fail status for each test case with expected vs actual output
5. **FeedbackPanel** - Display detected error patterns with GPT-4 explanations
6. **ProgressDashboard** - Visualize weakness trends, solved problems, mastery scores
7. **AuthProvider** - Handle Clerk authentication, protect routes

### Backend Modules

1. **ExecutionService** - Orchestrate Judge0 API calls, handle timeouts, retries
2. **ASTParser** - Parse code into Abstract Syntax Tree, extract features (complexity, loops, conditionals)
3. **PatternDetector** - Rule-based classifier detecting 6 error categories from AST features
4. **FeedbackGenerator** - Interface with GPT-4o-mini/4o to generate educational explanations
5. **RecommendationEngine** - Calculate mastery scores, select next problems based on weaknesses
6. **UserService** - CRUD operations for user profiles, attempts, weakness tracking
7. **ProblemService** - Query problems by tags/difficulty, retrieve test cases

### Data Models

1. **User** - id, clerk_user_id, email, created_at, total_problems_solved
2. **Problem** - id, title, description, difficulty, optimal_complexity, test_cases (JSONB), tags
3. **Submission** - id, user_id, problem_id, code, passed, execution_time_ms, test_results (JSONB)
4. **WeaknessPattern** - id, user_id, pattern_type, frequency, last_occurred, mastery_score

---

## 7. Key UI/UX Considerations

### Core UX Principles

1. **Immediate Clarity** - Users should understand detected weaknesses within 5 seconds of reading feedback
2. **Minimal Friction** - Submit code → see results in <10 seconds (P95 latency target)
3. **Progress Visibility** - Every submission updates dashboard in real-time to show measurable improvement
4. **Educational Focus** - Explanations connect mistakes to CS concepts, not just "wrong"
5. **Trust Through Transparency** - Show specific test cases that failed, exact line numbers for issues

### Key Interaction Patterns

- **Problem Selection Flow:** List → Detail → Code → Submit → Feedback → Next Problem
- **Feedback Review:** Expandable sections for each pattern (overview → detailed explanation → how to fix)
- **Dashboard Exploration:** Hover tooltips on charts, click weakness to see related problems
- **Error Guidance:** Inline annotations in code editor pointing to problematic lines (future)

### Responsive Design

- **Desktop-first:** Primary use case is on laptop during practice sessions
- **Minimum viewport:** 1280×720px (standard laptop)
- **Mobile:** Not optimized for MVP (web-first approach)

---

## 8. Coding Standards & Quality Criteria

### Style Guide

- **Python:** PEP 8 (enforced by Black formatter)
- **JavaScript/TypeScript:** Airbnb JavaScript Style Guide (enforced by ESLint/Prettier)

### Formatter

- **Python:** Black 23.11.0 (config in `pyproject.toml`)
- **JavaScript/TypeScript:** Prettier 3.1.0 (config in `.prettierrc`)

### Linter

- **Python:** Ruff 0.1.6 (config in `ruff.toml`)
- **JavaScript/TypeScript:** ESLint 8.54.0 (config in `.eslintrc.js`)

### Key Patterns

- **Repository Pattern** for data access (abstract DB operations)
- **DRY Principle** - Reusable functions for AST analysis, pattern detection
- **Dependency Injection** for services (easier testing, mocking)
- **Error Handling** - Explicit try-catch blocks, structured error responses

### File Naming Conventions

- **Python:** `snake_case.py` (e.g., `pattern_detector.py`)
- **React Components:** `PascalCase.tsx` (e.g., `CodeEditor.tsx`)
- **Utilities:** `camelCase.ts` (e.g., `formatTime.ts`)
- **Tests:** `test_*.py` or `*.test.tsx` (adjacent to source files)

### Top 5 Quality Criteria Focus

1. **Reliability** - Code execution must work 95%+ of the time, graceful degradation on failures
2. **Testability** - All functions unit testable, clear interfaces, mockable dependencies
3. **Security** - Sandboxed execution, JWT validation, no PII leakage, prompt injection protection
4. **Cost-efficiency** - GPT-4 hybrid model saves 74% costs, caching reduces redundant API calls
5. **Maintainability** - Clear module boundaries, comprehensive docstrings, architecture documentation

### Other Standards

- **Docstrings Required:** All functions (Google-style format for Python, JSDoc for TypeScript)
- **Type Hints:** Python 3.11+ type hints for all function signatures
- **Commit Messages:** Conventional Commits format (`feat:`, `fix:`, `docs:`, etc.)

---

## 9. Testing Strategy

### Required Test Types

1. **Unit Tests** - Individual functions (pattern detector, AST parser, recommender logic)
2. **Integration Tests** - API endpoints with mocked external services (Judge0, OpenAI)
3. **E2E Tests** - Full user flows (signup → solve → feedback) in real browser

### Testing Frameworks & Versions

- **Backend Unit/Integration:** pytest 7.4.0, pytest-asyncio 0.21.0
- **Frontend Unit:** Jest 29.6.2, React Testing Library 14.1.0
- **E2E:** Playwright 1.40.0

### Minimum Code Coverage

- **Backend:** 80% line coverage (measured by pytest-cov)
- **Frontend:** 75% coverage (measured by Jest)
- **Critical paths:** 100% coverage (authentication, code execution, pattern detection)

### Testing Conventions

- **AAA Pattern:** Arrange-Act-Assert structure for all unit tests
- **Test Files:** Adjacent to source (e.g., `pattern_detector.py` → `test_pattern_detector.py`)
- **Fixtures:** Shared fixtures in `tests/conftest.py` (pytest) or `setupTests.ts` (Jest)
- **Mocking:** Mock all external APIs (Judge0, OpenAI) to avoid costs and flakiness

### Verification Approach

- **CI/CD Pipeline:** GitHub Actions runs all tests on every PR
- **Pre-commit Hooks:** Run linters and formatters before commit (using `pre-commit` framework)
- **Manual QA:** Week 7 and Week 14 user testing with 5-8 real users
- **Golden Set:** 50 standardized test cases for pattern detection regression testing

---

## 10. Initial Setup Steps

### Prerequisites

- Git installed
- [Python 3.11+ OR Node.js 18+ LTS] (depending on chosen stack)
- PostgreSQL 15+ running locally or accessible via Railway
- Redis 7+ running locally or accessible via Railway
- Judge0 API key (free tier: 50 requests/day)
- OpenAI API key (pay-as-you-go)
- Clerk account and API keys

### Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/MariamKhoKh/cs-ai-2025-team-ai4ce.git
cd cs-ai-2025-team-ai4ce
```
# 2. Navigate to backend directory
```
cd backend
```
# 3. Create virtual environment (if Python)
```
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
# 4. Install dependencies
```
pip install -r requirements.txt  # (if Python)
```
# OR
```
npm install  # (if Node.js)
```
# 5. Copy environment template
```
cp .env.example .env
```
# 6. Edit .env file with required credentials
# Required variables:
###  - DATABASE_URL=postgresql://user:pass@host:5432/dbname
###  - REDIS_URL=redis://localhost:6379
###  - JUDGE0_API_KEY=your_judge0_key
###  - OPENAI_API_KEY=sk-...
###  - CLERK_SECRET_KEY=sk_test_...

# 7. Run database migrations
```
alembic upgrade head  # (if using Alembic)
```
# 8. Seed database with 30 problems
python scripts/seed_problems.py

# 9. Run tests to verify setup
pytest tests/

# 10. Start development server
```
uvicorn main:app --reload  # (if FastAPI)
```
# OR
```
npm run dev  # (if Node.js)
```

### Frontend Setup


# 1. Navigate to frontend directory
```
cd frontend
```
# 2. Install dependencies
```
npm install
```
# 3. Copy environment template
```
cp .env.example .env.local
```
# 4. Edit .env.local with required variables
# Required:
#   - VITE_API_URL=http://localhost:8000
#   - VITE_CLERK_PUBLISHABLE_KEY=pk_test_...

# 5. Run tests
```
npm test
```
# 6. Start development server
```
npm run dev
```

### Verification

- **Backend:** Visit http://localhost:8000/docs (FastAPI auto-generated docs)
- **Frontend:** Visit http://localhost:5173 (Vite default port)
- Test login flow with Clerk authentication
- Submit a test problem to verify end-to-end pipeline

---

## 11. Key Architectural Decisions

### Decision 1: Flask → FastAPI (Backend Framework)

**Rationale:** Initially considered Flask for familiarity, but switched to FastAPI for native async/await support. Need to call Judge0 (6s execution) and OpenAI (3s generation) concurrently to meet <10s latency target. FastAPI's async enables parallel API calls where possible, plus automatic API documentation (Swagger) and Pydantic validation reduce boilerplate.

**Trade-off Accepted:** Steeper learning curve (async programming) worth it for performance gains and built-in features.

### Decision 2: Custom ML Model → Rule-Based + GPT-4 Hybrid

**Rationale:** Week 2 plan was Random Forest classifier trained on 500+ labeled examples. After Week 3-4 prototyping, realized we don't have time to collect/label that data. Pivoted to rule-based classifier detecting 6 core patterns via AST analysis (e.g., nested loops = O(n²), missing null checks). GPT-4 generates educational explanations. Rule-based achieves 70-75% accuracy (vs 85-90% for ML) but can launch 3 weeks earlier.

**Trade-off Accepted:** Lower accuracy acceptable to meet timeline. Can train ML model post-course with real user data.

### Decision 3: MongoDB → PostgreSQL (Database)

**Rationale:** Week 2 plan used MongoDB for flexibility. Week 3 data modeling revealed strong relational structure (users → submissions → patterns). PostgreSQL foreign keys enforce data integrity (prevents orphaned records), complex JOINs easier for analytics (e.g., "users who improved fastest"). JSON columns (JSONB) handle semi-structured data (test results, AST metrics).

**Trade-off Accepted:** Less schema flexibility, but stricter integrity prevents bugs. Migrations manageable with Alembic.

### Decision 4: GPT-4o Only → GPT-4o-mini (90%) + GPT-4o (10%)

**Rationale:** Week 3 cost projection showed $45/month for GPT-4o only (90% over $50 semester budget). Testing showed GPT-4o-mini quality 85% as good for simple patterns (edge cases, syntax) at 10× lower cost ($0.00144 vs $0.036/query). Reserve GPT-4o for complex patterns (ambiguous errors, advanced algorithmic explanations).

**Trade-off Accepted:** Slightly lower quality on 10% of queries, but 74% cost reduction ($12/month vs $45/month) keeps us within budget.

### Decision 5: Judge0 Cloud → Self-Hosted (Deferred)

**Rationale:** Self-hosting Judge0 saves $20/month and reduces latency (500ms vs 6s), but requires Docker setup, security hardening (sandboxing, resource limits), ongoing maintenance. For MVP with <50 users, cloud API sufficient. Self-host only if we scale to 100+ daily active users post-course.

**Trade-off Accepted:** Higher cost and latency acceptable for faster MVP launch. Can migrate later if validated.

---

## 12. Project Documentation

### Core Documentation Files

- **Project Overview (this document):** `./docs/prd-full.md`
- **Refined Capstone Proposal:** `./docs/proposal-v2.md`
- **Architecture Explanation:** `./docs/architecture-v2.md`
- **Feature Roadmap:** `./docs/feature-roadmap.md`
- **Evaluation Plan:** `./docs/evaluation-plan-v2.md`
- **Token Usage & Cost Model:** `./docs/cost-model.md`
- **Prioritized Backlog:** `./docs/backlog-v2.md`

### Technical Documentation

- **API Documentation:** `./docs/api.md` (OpenAPI spec at `/docs` endpoint)
- **Database Schema:** `./docs/database-schema.md`
- **Testing Guide:** `./docs/testing.md`
- **Deployment Guide:** `./docs/deployment.md`

### Research Documentation

- **User Testing Round 1 (Week 7):** `./research/user-testing-round1.md`
- **User Testing Round 2 (Week 14):** `./research/user-testing-round2.md`
- **Golden Set Test Cases:** `./tests/golden-set/README.md`

---

## 13. Repository Link

**GitHub Repository:** https://github.com/MariamKhoKh/cs-ai-2025-team-ai4ce

### Repository Structure

```
cs-ai-2025-team-ai4ce/
├── backend/              # FastAPI backend
│   ├── api/             # API endpoints
│   ├── services/        # Business logic
│   ├── models/          # Database models
│   ├── analysis/        # AST parser, pattern detector
│   ├── tests/           # Unit and integration tests
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   └── tests/       # Frontend tests
│   └── package.json
├── docs/                # All documentation
├── research/            # User testing reports
├── tests/               # Golden set, E2E tests
├── scripts/             # Setup and seed scripts
└── README.md
```

---

## 14. Dependencies & Third-Party Services

### External Services

#### 1. Judge0 API (Code Execution)

- **Purpose:** Sandboxed code execution with security isolation
- **Integration:** REST API, POST /submissions
- **Configuration:** 5s timeout, 128MB memory limit, no network/file access
- **Credentials:** API key (free tier: 50 executions/day)
- **Rate Limits:** Free tier sufficient for MVP testing, upgrade to $0.002/execution for production
- **Fallback:** Piston API (alternative execution service tested)

#### 2. OpenAI API (GPT-4o/mini)

- **Purpose:** Generate educational feedback explanations
- **Integration:** REST API via `openai` Python SDK
- **Configuration:** 
  - GPT-4o-mini: $0.00015/1K input, $0.0006/1K output (90% of queries)
  - GPT-4o: $0.005/1K input, $0.015/1K output (10% of queries)
  - Max tokens: 500, Temperature: 0.3 (consistent responses)
- **Credentials:** API key (pay-as-you-go)
- **Rate Limits:** 3 requests/minute (free tier), sufficient for testing
- **Cost Tracking:** Monitor daily spend, alert if >$2/day

#### 3. Clerk (Authentication)

- **Purpose:** User authentication and JWT token management
- **Integration:** React SDK (frontend), JWT validation (backend)
- **Configuration:** Email + password, Google OAuth, magic links
- **Credentials:** Publishable key (frontend), Secret key (backend)
- **Rate Limits:** Free tier: 10,000 monthly active users
- **Security:** JWTs expire after 1 hour, automatic refresh

#### 4. Railway (Infrastructure)

- **Purpose:** Hosting backend (FastAPI), PostgreSQL, Redis
- **Integration:** GitHub auto-deploy on push to main branch
- **Configuration:** Dockerfile for backend, managed PostgreSQL/Redis
- **Credentials:** Railway API key (for CLI deployments)
- **Cost:** Free $5 credit/month, expect $10/month actual usage

#### 5. Vercel (Frontend Hosting)

- **Purpose:** Host React SPA with global CDN
- **Integration:** GitHub auto-deploy on push to main branch
- **Configuration:** Build command: `npm run build`, Output: `dist/`
- **Credentials:** Vercel API token (for CLI deployments)
- **Cost:** Free tier (unlimited bandwidth, 100GB-hours execution)

### Required API Keys/Credentials

Create `.env` file with:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/codementor
REDIS_URL=redis://localhost:6379
JUDGE0_API_KEY=your_judge0_api_key
OPENAI_API_KEY=sk-...your_openai_key
CLERK_SECRET_KEY=sk_test_...your_clerk_secret
CLERK_PUBLISHABLE_KEY=pk_test_...your_clerk_publishable
RAILWAY_TOKEN=your_railway_token
```

### Where to Obtain Credentials

- **Judge0:** Sign up at https://rapidapi.com/judge0-official/api/judge0-ce
- **OpenAI:** https://platform.openai.com/api-keys
- **Clerk:** https://dashboard.clerk.com → Create application
- **Railway:** https://railway.app → New project
- **Vercel:** https://vercel.com → Import Git repository

---

## 15. Security Considerations

### Authentication Method

- **Primary:** JWT tokens via Clerk (OAuth 2.0 flow)
- **Token Lifespan:** 1 hour (automatic refresh)
- **Storage:** Stored in memory (not localStorage) to prevent XSS attacks
- **Validation:** Backend validates JWT signature using Clerk's public key on every protected endpoint

### Authorization Approach

- **Role-Based:** Simple user role (no admin for MVP)
- **Resource Ownership:** Users can only access their own submissions, profiles, progress
- **Endpoint Protection:** All `/api/users/{id}/*` endpoints validate `user_id` matches JWT subject

### Data Protection

- **In Transit:** TLS 1.3 for all communication (enforced by Vercel/Railway)
- **At Rest:** Database encryption via Railway managed PostgreSQL (AES-256)
- **PII Handling:** Email addresses stored, no SSNs or payment info
- **Code Privacy:** User submissions not shared with other users, anonymized for ML training (opt-in)

### Key Security Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Code Injection** | Malicious code access file system/network | Judge0 sandbox: no file/network access, 5s timeout, 128MB limit |
| **Prompt Injection** | Manipulate GPT-4 via crafted code comments | Treat all user input as data, not instructions; validate before sending |
| **XSS (Cross-Site Scripting)** | Steal JWT tokens via malicious scripts | React auto-escapes; JWT in memory only; Content Security Policy headers |
| **SQL Injection** | Unauthorized database access | SQLAlchemy ORM with parameterized queries (no raw SQL) |
| **CSRF (Cross-Site Request Forgery)** | Unauthorized actions on behalf of user | SameSite cookies, CORS restricted to frontend domain |
| **Rate Limit Bypass** | Abuse API to exhaust resources/costs | Rate limiting: 20 submissions/hour per user, 10 requests/min globally |
| **PII Leakage** | Accidental exposure of user data | Audit logs, access control, no PII in error messages |

### Compliance Requirements

- **Student Project:** No GDPR/HIPAA compliance required for MVP
- **Data Retention:** User can request data deletion (GDPR-style) via support email
- **Future:** If commercialized, will need SOC2 compliance for enterprise customers

---

## 16. Performance Requirements

### Load Capacity

- **Development Phase (Weeks 3-9):** Support 5 concurrent users (team testing)
- **Production Phase (Weeks 10-15):** Support 20 concurrent users (8 active testers × 2-3 problems each)
- **Daily Query Volume:** 60-100 code submissions/day during user testing weeks

### Response Time Targets

- **Code Execution:** <6 seconds for 95% of submissions (Judge0 API latency)
- **Pattern Detection:** <500ms for AST parsing + classification
- **Feedback Generation:** <3 seconds for GPT-4 explanation (P50), <5 seconds (P95)
- **Total Submission Flow:** <10 seconds (P95) from submit click to feedback displayed
- **Page Load:** <1 second for problem list and dashboard pages
- **Database Queries:** <100ms for all queries (P95)

### Scalability Approach

- **Horizontal Scaling Ready:** FastAPI backend stateless, can scale to multiple Railway instances
- **Caching Strategy:** Redis for:
  - Problem descriptions (250 tokens saved per query)
  - Repeated explanations for identical error patterns (40% hit rate expected)
  - User session data
- **Database Optimization:** Indexes on `user_id`, `problem_id`, `created_at` for fast lookups
- **Load Balancing:** Railway provides automatic load balancing for multi-instance deployments

### Resource Constraints

- **Semester Budget:** <$50 total (currently projecting $36-59 with optimizations)
- **API Costs:** 
  - OpenAI: $31.54 projected (with caching and hybrid model)
  - Judge0: Free tier (50/day) → upgrade to paid if exceed
- **Hosting:** Railway free $5 credit covers development, expect $10/month production

---

## 17. Monitoring & Observability

### Logging Strategy

- **Format:** Structured JSON logs with fields: `timestamp`, `level`, `request_id`, `user_id`, `endpoint`, `latency_ms`, `error`
- **Levels:** ERROR (failures), WARN (degraded performance), INFO (normal operations), DEBUG (development)
- **Backend Logging:** Python `logging` module, output to stdout (captured by Railway)
- **Frontend Logging:** Console errors captured by Sentry (browser SDK)
- **Retention:** 30 days (Railway default)

### Monitoring Tools

- **Sentry (Free Tier):** Error tracking and alerting
  - Frontend errors (React errors, API failures)
  - Backend exceptions (unhandled errors, validation failures)
  - 5,000 events/month free
- **Custom Dashboard:** Google Sheets for cost tracking
  - Daily: Query count, GPT-4 distribution (mini vs full), total cost
  - Weekly: Active users, submissions, pattern detection accuracy
- **Railway Metrics:** Built-in CPU, memory, request count

### Key Metrics Tracked

| Metric | Target | Dashboard | Alert Threshold |
|--------|--------|-----------|-----------------|
| **Error Rate** | <5% | Sentry | >10% over 1 hour |
| **API Latency (P95)** | <10s | Railway | >15s sustained |
| **Code Execution Success** | >95% | Backend logs | <90% over 1 day |
| **GPT-4 Cost/Day** | <$2 | Google Sheets | >$2.50 |
| **Pattern Detection Accuracy** | >75% | Weekly review | <70% on golden set |
| **User Satisfaction** | >
