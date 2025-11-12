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
| **Language (Backend)** | Python | 3.11.7 | Stable LTS release, type hints support |
| **Language (Frontend)** | TypeScript | 5.2.2 | Type safety for React components |
| **Backend Framework** | FastAPI | 0.104.1 | High-performance async API framework |
| **Frontend Framework** | React | 18.2.0 | Component-based UI with hooks |
| **Build Tool** | Vite | 4.5.0 | Fast dev server and optimized builds |
| **UI Library** | Tailwind CSS | 3.3.5 | Utility-first CSS framework |
| **UI Components** | shadcn/ui | 0.8.0 | Accessible React components |
| **Code Editor** | Monaco Editor | 0.44.0 | VS Code-based in-browser editor |
| **Database** | PostgreSQL | 15.4 | Relational database (Railway hosted) |
| **ORM** | SQLAlchemy | 2.0.23 | Python SQL toolkit and ORM |
| **Cache** | Redis | 7.2.3 | In-memory data store for caching |
| **Authentication** | Clerk | 4.27.1 | OAuth2 & JWT management |
| **Code Execution** | Judge0 CE | API v1.13.0 | Sandboxed multi-language execution |
| **AI/LLM** | OpenAI API | GPT-4o-mini / GPT-4o | 90% mini / 10% full for cost optimization |
| **HTTP Client** | httpx | 0.25.1 | Async HTTP client for Python |
| **Async Tasks** | asyncio | Built-in | Native Python async/await |
| **Testing (Backend)** | pytest | 7.4.3 | Unit & integration test framework |
| **Testing (Backend - Async)** | pytest-asyncio | 0.21.1 | Async test support |
| **Testing (Frontend)** | Jest | 29.7.0 | JavaScript testing framework |
| **Testing (React)** | React Testing Library | 14.1.2 | Component testing utilities |
| **Testing (E2E)** | Playwright | 1.40.1 | Cross-browser automation |
| **Load Testing** | k6 | 0.47.0 | Performance and load testing |
| **Code Quality (Python)** | Black | 23.11.0 | Python code formatter |
| **Code Quality (Python)** | Ruff | 0.1.6 | Fast Python linter |
| **Code Quality (TS)** | ESLint | 8.54.0 | TypeScript/JavaScript linter |
| **Code Quality (TS)** | Prettier | 3.1.0 | Code formatter for TS/JS |
| **DevOps** | Docker | 24.0.7 | Container platform |
| **Deployment (Frontend)** | Vercel | N/A | Serverless deployment, auto-deploy |
| **Deployment (Backend)** | Railway | N/A | Container hosting with auto-deploy |
| **Version Control** | Git | 2.42+ | Distributed version control |
| **CI/CD** | GitHub Actions | N/A | Automated testing and deployment |
| **Monitoring (Errors)** | Sentry | 1.38.0 | Error tracking and monitoring |
| **Monitoring (Metrics)** | Prometheus | 2.48.0 | Metrics collection |
| **Monitoring (Visualization)** | Grafana | 10.2.0 | Metrics dashboards |
| **Database Migrations** | Alembic | 1.12.1 | SQLAlchemy migration tool |
| **Environment Variables** | python-dotenv | 1.0.0 | .env file management |
| **Data Validation** | Pydantic | 2.5.0 | Data validation using Python type hints |
| **CORS Middleware** | fastapi-cors | Built-in | Cross-origin resource sharing |

---

## 5. High-Level Architecture

**Architecture Style:** Modular monolith backend + Single Page Application (SPA) frontend with hybrid AI/code execution services.

**Key Characteristics:**
- **Backend:** FastAPI modular monolith with service-oriented design
- **Frontend:** React SPA with component-based architecture
- **Integration:** External APIs for code execution (Judge0) and AI feedback (OpenAI)
- **Data Flow:** Synchronous API calls with async processing for long-running operations
- **Scalability:** Stateless services with Redis caching for horizontal scaling

### Architecture Diagram

```mermaid
graph TB
    User[User Browser]
    FE[React FrontendVercelPort: 5173]
    BE[FastAPI BackendRailwayPort: 8000]
    DB[(PostgreSQLRailwayPort: 5432)]
    Cache[(RedisRailwayPort: 6379)]
    Judge0[Judge0 APIExternal ServiceCode Execution]
    OpenAI[OpenAI APIGPT-4o/miniAI Feedback]
    Clerk[Clerk AuthJWT Validation]
    
    User -->|HTTPS/WSS| FE
    FE -->|REST API| BE
    FE -->|OAuth2| Clerk
    BE -->|Validate JWT| Clerk
    BE -->|SQL Queries| DB
    BE -->|GET/SET| Cache
    BE -->|POST /submissions| Judge0
    BE -->|POST /chat/completions| OpenAI
    
    subgraph Analysis Pipeline
        BE -->|1. Submit Code| Judge0
        Judge0 -->|2. Execution Results| BE
        BE -->|3. Parse AST| BE
        BE -->|4. Detect Patterns| BE
        BE -->|5. Generate Prompt| OpenAI
        OpenAI -->|6. AI Feedback| BE
        BE -->|7. Store Results| DB
        BE -->|8. Cache Response| Cache
    end
    
    subgraph Backend Services
        ExecSvc[ExecutionService]
        ASTSvc[ASTParser]
        PatternSvc[PatternDetector]
        FeedbackSvc[FeedbackGenerator]
        RecoSvc[RecommendationEngine]
        UserSvc[UserService]
        ProblemSvc[ProblemService]
    end
```

### Layer Responsibilities

- **Presentation Layer (React SPA):**
  - User interface components
  - Client-side routing
  - State management (React Context/hooks)
  - API integration via fetch/axios

- **Application Layer (FastAPI):**
  - RESTful API endpoints
  - Business logic orchestration
  - Service layer pattern
  - Request validation and serialization

- **Data Layer (PostgreSQL + Redis):**
  - Persistent storage (PostgreSQL)
  - Session and cache storage (Redis)
  - Database migrations (Alembic)
  - Query optimization

- **Integration Layer:**
  - Judge0 API client for code execution
  - OpenAI API client for AI feedback
  - Clerk API for authentication validation

- **Monitoring & Logging:**
  - Application logs (structured JSON)
  - Error tracking (Sentry)
  - Metrics collection (Prometheus)
  - Visualization (Grafana)

---

## 6. Core Components/Modules

### Frontend Modules

**ProblemList Component:**
- Browse and filter available coding problems
- Display problem difficulty, tags, and completion status
- Search functionality with debouncing
- Pagination for large datasets

**ProblemDetail Component:**
- Display problem description, constraints, and examples
- Show starter code template
- Render test cases (public only)
- Track user's previous submissions

**CodeEditor Component:**
- Monaco editor integration with Python syntax highlighting
- Auto-completion and IntelliSense
- Line numbers and minimap
- Submit code button with loading state

**TestResults Component:**
- Display pass/fail status for each test case
- Show expected vs. actual output
- Execution time and memory usage
- Error messages and stack traces

**FeedbackPanel Component:**
- AI-generated explanations of mistakes
- Pattern detection results with visual indicators
- Actionable improvement suggestions
- Links to related concepts/resources

**ProgressDashboard Component:**
- Weakness trend charts (line/bar graphs via Recharts)
- Problem solving statistics
- Mastery scores per error pattern
- Recommended next problems

**AuthProvider Component:**
- Clerk authentication integration
- Protected route wrapper
- User profile management
- Session handling

### Backend Modules

**ExecutionService:**
- Orchestrate Judge0 API calls
- Handle submission queuing
- Parse execution results
- Error handling and retry logic

**ASTParser:**
- Parse Python code into Abstract Syntax Tree
- Extract code features (loop types, conditionals, function calls)
- Detect cyclomatic complexity
- Identify potential time/space complexity

**PatternDetector:**
- Implement 6 core error pattern detectors:
  1. Missing edge cases (null, empty, boundary)
  2. Suboptimal time complexity
  3. Wrong data structure choice
  4. Off-by-one errors
  5. Missing input validation
  6. Inefficient loops/redundant operations
- Calculate pattern frequency
- Update mastery scores

**FeedbackGenerator:**
- Construct prompts for GPT-4o-mini/4o
- Implement 90/10 routing logic (mini for standard, full for complex)
- Parse and format AI responses
- Fallback to rule-based feedback on API failure

**RecommendationEngine:**
- Analyze user weakness patterns
- Calculate problem relevance scores
- Generate personalized problem queue
- Balance difficulty and pattern coverage

**UserService:**
- CRUD operations for user data
- Track total problems solved
- Update user progress metrics
- Manage user preferences

**ProblemService:**
- Query problems by filters (difficulty, tags, patterns)
- Retrieve test cases (public and hidden)
- Cache frequently accessed problems
- Seed initial problem database

### Data Models

**User Model:**
```python
id: UUID (Primary Key)
clerk_user_id: String (Unique, indexed)
email: String (Unique)
created_at: Timestamp
updated_at: Timestamp
total_problems_solved: Integer (default: 0)
current_streak: Integer (default: 0)
```

**Problem Model:**
```python
id: UUID (Primary Key)
title: String (indexed)
slug: String (Unique, indexed)
description: Text
difficulty: Enum (Easy, Medium, Hard)
test_cases: JSONB (array of {input, expected_output, is_hidden})
tags: JSONB (array of strings)
starter_code: Text
optimal_complexity_time: String (e.g., "O(n)")
optimal_complexity_space: String (e.g., "O(1)")
target_patterns: JSONB (array of pattern types)
created_at: Timestamp
```

**Submission Model:**
```python
id: UUID (Primary Key)
user_id: UUID (Foreign Key -> User)
problem_id: UUID (Foreign Key -> Problem)
code: Text
language: String (default: "python")
passed: Boolean
execution_time_ms: Integer
memory_kb: Integer
test_results: JSONB (array of test case results)
detected_patterns: JSONB (array of pattern objects)
ai_feedback: Text (nullable)
submitted_at: Timestamp
```

**WeaknessPattern Model:**
```python
id: UUID (Primary Key)
user_id: UUID (Foreign Key -> User, indexed)
pattern_type: Enum (6 pattern types)
frequency: Integer (count of occurrences)
last_occurred: Timestamp
mastery_score: Float (0.0 to 1.0)
problems_with_pattern: JSONB (array of problem IDs)
created_at: Timestamp
updated_at: Timestamp
```

---

## 7. Key UI/UX Considerations

**Integrated Workspace:**
- Single-screen layout combining problem description, code editor, and results
- Collapsible panels to maximize editor space
- Persistent editor state across sessions

**Simplicity & Focus:**
- Minimal navigation with 3 main views: Problems, Editor, Dashboard
- Clean, distraction-free interface during coding
- Progressive disclosure of advanced features

**Responsive Design:**
- Desktop-first approach (1920x1080 primary target)
- Tablet support (1024x768 minimum)
- Mobile view for progress tracking only (no code editing)

**Real-time Feedback:**
- Immediate syntax highlighting and error detection
- Live execution status updates
- Smooth transitions between states (loading, success, error)

**Educational Focus:**
- Color-coded pattern indicators (red = critical, yellow = improvement, green = mastered)
- Tooltips explaining technical terms
- Links to educational resources for each pattern

**Accessibility:**
- WCAG 2.1 AA compliance
- Keyboard navigation support
- High contrast mode option
- Screen reader compatible

**Performance Perception:**
- Optimistic UI updates
- Skeleton loaders for async operations
- Progress indicators for long-running tasks (>2s)

---

## 8. Coding Standards & Quality Criteria

**Style Guides:**
- **Python:** PEP 8 + Black formatter (line length: 88 characters)
- **TypeScript/JavaScript:** Airbnb JavaScript Style Guide + Prettier
- **React:** Functional components with hooks, no class components

**Formatters:**
- **Black:** `pyproject.toml` configuration for consistent Python formatting
- **Prettier:** `.prettierrc` configuration (2-space indent, single quotes, trailing commas)

**Linters:**
- **Ruff:** Fast Python linter replacing Flake8, isort, pyupgrade (config in `pyproject.toml`)
- **ESLint:** TypeScript-aware linting (config in `.eslintrc.js`)
- **mypy:** Static type checking for Python (strict mode)

**Key Architectural Patterns:**
- **Repository Pattern:** Data access abstraction layer
- **Dependency Injection:** Service instantiation via FastAPI's Depends()
- **Factory Pattern:** Object creation for complex entities
- **Strategy Pattern:** Multiple feedback generation strategies
- **DRY Principle:** No code duplication, shared utilities

**File Naming Conventions:**
- **Python:** `snake_case.py` (e.g., `pattern_detector.py`)
- **TypeScript:** `PascalCase.tsx` for components (e.g., `CodeEditor.tsx`)
- **TypeScript:** `camelCase.ts` for utilities (e.g., `apiClient.ts`)
- **Tests:** `test_*.py` or `*.test.tsx`

**Top 5 Quality Criteria Focus:**
1. **Testability:** All business logic must be unit testable with >80% coverage
2. **Reliability:** Error handling for all external API calls with fallback mechanisms
3. **Security:** Input validation, SQL injection prevention, XSS protection
4. **Maintainability:** Clear separation of concerns, modular design, comprehensive docs
5. **Cost-efficiency:** Optimize LLM token usage, cache repeated queries, minimize API calls

**Other Key Standards:**
- All public functions/classes must have docstrings (Google style for Python, JSDoc for TS)
- Type hints required for all Python function signatures
- PropTypes or TypeScript interfaces for all React components
- Git commit messages follow Conventional Commits (feat:, fix:, docs:, etc.)
- No TODO comments in main branch; create GitHub issues instead
- Maximum function length: 50 lines (refactor if longer)

---

## 9. Testing Strategy

**Required Test Types:**
1. **Unit Tests:** Individual functions/methods (target: 85% coverage)
2. **Integration Tests:** API endpoints + database + external services (target: 75% coverage)
3. **E2E Tests:** Critical user flows (5 key scenarios minimum)
4. **Load Tests:** Performance under expected load (20 concurrent users)

**Testing Frameworks & Versions:**
- **Backend Unit/Integration:** pytest 7.4.3 + pytest-asyncio 0.21.1
- **Frontend Unit:** Jest 29.7.0 + React Testing Library 14.1.2
- **E2E:** Playwright 1.40.1 (Chromium, Firefox, WebKit)
- **Load Testing:** k6 0.47.0
- **Coverage:** pytest-cov 4.1.0, Istanbul for Jest

**Minimum Code Coverage:**
- **Backend:** 80% overall, 100% for critical paths (ExecutionService, PatternDetector)
- **Frontend:** 75% overall, 100% for auth and submission flows
- **Integration Tests:** All API endpoints must have at least one test

**Testing Conventions:**
- **AAA Pattern:** Arrange, Act, Assert structure for all unit tests
- **Test File Location:** Adjacent to source files (`tests/` directory mirroring `src/`)
- **Test Naming:** `test_<function_name>_<scenario>_<expected_result>`
- **Fixtures:** Shared test data in `conftest.py` (pytest) or `setupTests.ts` (Jest)
- **Mocking:** Mock external APIs (Judge0, OpenAI) using pytest-mock / jest.mock
- **Database:** Use test database with transaction rollback after each test

**Verification Approach:**
- **Pre-commit Hooks:** Run linters and formatters locally (via pre-commit framework)
- **Pull Request Checks:** GitHub Actions runs all tests + coverage reports
- **Deployment Gate:** Tests must pass before deploy to staging/production
- **Nightly Runs:** Full E2E suite + load tests run daily

**Test Example Structure:**

```python
# Backend Unit Test (pytest)
def test_pattern_detector_identifies_missing_edge_case():
    # Arrange
    code = "def solution(arr): return arr[0]"
    detector = PatternDetector()
    
    # Act
    patterns = detector.analyze(code)
    
    # Assert
    assert PatternType.MISSING_EDGE_CASE in patterns
    assert patterns[PatternType.MISSING_EDGE_CASE].confidence > 0.8
```

```typescript
// Frontend Component Test (Jest + RTL)
describe('CodeEditor', () => {
  it('submits code when user clicks submit button', async () => {
    // Arrange
    const mockSubmit = jest.fn();
    render();
    
    // Act
    const editor = screen.getByRole('textbox');
    await userEvent.type(editor, 'def solution(): pass');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    // Assert
    expect(mockSubmit).toHaveBeenCalledWith('def solution(): pass');
  });
});
```

---

## 10. Initial Setup Steps

### Prerequisites
- Python 3.11.7 installed
- Node.js 18+ and npm 9+ installed
- Git 2.42+ installed
- Docker 24+ installed (optional, for local Judge0)
- PostgreSQL 15.4 (local or Railway account)
- Redis 7.2+ (local or Railway account)

### Backend Setup

```bash
# 1. Clone repository
git clone https://github.com/MariamKhoKh/cs-ai-2025-team-ai4ce.git
cd cs-ai-2025-team-ai4ce

# 2. Navigate to backend directory
cd backend

# 3. Create Python virtual environment
python3.11 -m venv venv

# 4. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install dependencies
pip install -r requirements.txt

# 7. Copy environment template
cp .env.example .env

# 8. Edit .env file with required values:
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
# REDIS_URL=redis://host:6379/0
# JUDGE0_API_KEY=your_judge0_key_here
# JUDGE0_API_URL=https://judge0-ce.p.rapidapi.com
# OPENAI_API_KEY=sk-your_openai_key_here
# CLERK_SECRET_KEY=sk_test_your_clerk_secret
# CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_key
# ENVIRONMENT=development

# 9. Run database migrations
alembic upgrade head

# 10. Seed initial problems
python scripts/seed_problems.py

# 11. Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 12. Verify backend is running
# Open http://localhost:8000/docs in browser (FastAPI Swagger UI)

# 13. Run tests
pytest tests/ -v --cov=app --cov-report=html
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory (from repo root)
cd frontend

# 2. Install npm dependencies
npm install

# 3. Copy environment template
cp .env.example .env.local

# 4. Edit .env.local file with required values:
# VITE_API_URL=http://localhost:8000
# VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_key

# 5. Run tests
npm test

# 6. Start development server
npm run dev

# 7. Verify frontend is running
# Open http://localhost:5173 in browser

# 8. Build for production (optional)
npm run build

# 9. Preview production build (optional)
npm run preview
```

### Verification Checklist

- [ ] Backend API docs accessible at http://localhost:8000/docs
- [ ] Frontend application loads at http://localhost:5173
- [ ] User can sign in via Clerk authentication
- [ ] Problem list displays 30 seeded problems
- [ ] Code editor renders with syntax highlighting
- [ ] Test submission executes and returns results
- [ ] All backend tests pass: `pytest tests/`
- [ ] All frontend tests pass: `npm test`

### Troubleshooting

**Database connection errors:**
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL format in .env
- Ensure database exists: `createdb codementor_dev`

**Redis connection errors:**
- Verify Redis is running: `redis-cli ping`
- Check REDIS_URL in .env
- Start Redis: `redis-server`

**Judge0 API errors:**
- Verify API key is valid
- Check rate limits (free tier: 50 requests/day)
- Test with curl: `curl -X GET https://judge0-ce.p.rapidapi.com/about`

**OpenAI API errors:**
- Verify API key starts with `sk-`
- Check account has credits
- Test with: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`

---

## 11. Key Architectural Decisions

### Decision 1: Database Choice - PostgreSQL

**Rationale:**
- **Relational integrity:** User-problem-submission relationships are naturally relational
- **JSONB support:** Flexible storage for test cases, detected patterns, and dynamic data without sacrificing query performance
- **ACID compliance:** Critical for submission history and progress tracking
- **Railway support:** Free tier with 500MB storage, automatic backups
- **Alternatives considered:** MongoDB (rejected: weak relationship support), SQLite (rejected: not production-ready for multi-user)

### Decision 2: Backend Framework - FastAPI

**Rationale:**
- **Async performance:** Native async/await for concurrent Judge0 and OpenAI API calls (2-3x faster than Flask)
- **Automatic OpenAPI docs:** Interactive API testing via Swagger UI at /docs
- **Type safety:** Pydantic models for request/response validation with IDE autocomplete
- **Modern Python:** Leverages Python 3.11+ type hints and performance improvements
- **Alternatives considered:** Django (rejected: overkill for API-only backend), Flask (rejected: no native async support)

### Decision 3: Feedback Engine - Hybrid AST + GPT-4o

**Rationale:**
- **Cost optimization:** 90% of queries use GPT-4o-mini ($0.15/1M input tokens vs. $5/1M for GPT-4o)
- **Accuracy balance:** Rule-based AST analysis catches obvious patterns deterministically
- **Educational quality:** GPT-4o provides nuanced explanations for complex errors
- **Fallback mechanism:** If OpenAI API fails, rule-based feedback still provides value
- **Token efficiency:** AST pre-analysis reduces prompt size by 40%
- **Alternatives considered:** Claude (rejected: higher cost), Llama 2 (rejected: self-hosting complexity), rule-based only (rejected: lacks educational depth)

### Decision 4: Authentication - Clerk

**Rationale:**
- **Zero backend auth code:** JWT validation handled entirely by Clerk SDK
- **OAuth2 providers:** Google, GitHub, Microsoft login out-of-box
- **Free tier:** 5,000 monthly active users sufficient for MVP
- **Security:** Automatic key rotation, session management, MFA support
- **Developer experience:** React hooks for protected routes, user metadata
- **Alternatives considered:** Auth0 (rejected: more complex pricing), NextAuth (rejected: requires manual JWT handling), Firebase Auth (rejected: ties to Firebase ecosystem)

### Decision 5: Code Execution - Judge0 Cloud API (MVP) vs. Self-hosted (Phase 2)

**Rationale for MVP:**
- **Rapid development:** No Docker/Kubernetes setup required
- **Sandboxing guaranteed:** Pre-configured secure execution environment
- **Multi-language support:** Future-proof for Java, C++, JavaScript support
- **Free tier:** 50 requests/day sufficient for 5 active testers
- **Known limitations:** 2-5s API latency, rate limits
- **Post-MVP plan:** Self-host Judge0 CE on Railway for <200ms latency and unlimited requests at $5/month
- **Alternatives considered:** AWS Lambda (rejected: cold start latency), Piston API (rejected: less mature), custom sandbox (rejected: security risks)

---

## 12. Project Documentation

**Core Documentation:**
- **Project Overview:** `./docs/prd-full.md` - Complete product requirements document
- **Architecture Details:** `./docs/architecture-v2.md` - System design and component interactions
- **API Reference:** `./docs/api.md` - Endpoint specifications, request/response schemas
- **Testing Guidelines:** `./docs/testing.md` - Testing strategy, conventions, and examples
- **Deployment Guide:** `./docs/deployment.md` - Setup instructions for dev, staging, production
- **Feature Backlog:** `./docs/backlog-v2.md` - Prioritized features and roadmap

**Technical Documentation:**
- **Database Schema:** `./docs/schema.md` - Entity-relationship diagram and model definitions
- **Pattern Detection:** `./docs/pattern-detection.md` - Algorithm details for 6 error patterns
- **AI Prompt Engineering:** `./docs/prompts.md` - GPT-4 prompt templates and optimization
- **Performance Tuning:** `./docs/performance.md` - Caching strategy, query optimization

**User Research:**
- **UX Testing Round 1:** `./research/user-testing-round1.md` - Week 7 usability findings
- **UX Testing Round 2:** `./research/user-testing-round2.md` - Week 14 iteration results
- **User Personas:** `./research/personas.md` - Target user profiles and scenarios

**Development Guides:**
- **Contributing Guide:** `./CONTRIBUTING.md` - Code contribution workflow
- **Style Guide:** `./docs/style-guide.md` - Coding standards and best practices
- **Local Development:** `./docs/local-dev.md` - IDE setup, debugging tips
- **Troubleshooting:** `./docs/troubleshooting.md` - Common issues and solutions

**Meeting Notes:**
- **Weekly Standups:** `./meeting-notes/standups/` - Sprint progress and blockers
- **Architecture Reviews:** `./meeting-notes/architecture/` - Design decision discussions

---

## 13. Repository Link

**Primary Repository:** [https://github.com/MariamKhoKh/cs-ai-2025-team-ai4ce](https://github.com/MariamKhoKh/cs-ai-2025-team-ai4ce)

**Branch Strategy:**
- `main` - Production-ready code, protected branch
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `hotfix/*` - Emergency production fixes

**Repository Structure:**
```
cs-ai-2025-team-ai4ce/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── public/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── docs/
├── research/
├── .github/
│   └── workflows/
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

## 14. Dependencies & Third-Party Services

### External APIs

**Judge0 CE API:**
- **Purpose:** Sandboxed code execution for Python submissions
- **Integration:** REST API via httpx client
- **Endpoint:** https://judge0-ce.p.rapidapi.com
- **Authentication:** RapidAPI key in header `X-RapidAPI-Key`
- **Rate Limits:** Free tier - 50 requests/day, Paid - Unlimited at $0.004/request
- **Required Credentials:** `JUDGE0_API_KEY` (obtain from https://rapidapi.com/judge0-official/api/judge0-ce)
- **Fallback:** Queue failed submissions for retry, display cached results for repeated code

**OpenAI API:**
- **Purpose:** Educational feedback generation via GPT-4o-mini and GPT-4o
- **Integration:** Official Python SDK `openai==1.3.5`
- **Endpoint:** https://api.openai.com/v1/chat/completions
- **Authentication:** Bearer token in header `Authorization: Bearer sk-...`
- **Rate Limits:** Tier 1 - 500 RPM, 200,000 TPM
- **Cost Management:** 
  - GPT-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens (90% of requests)
  - GPT-4o: $5/1M input tokens, $15/1M output tokens (10% of complex cases)
  - Daily budget cap: $2.00 (alerts at $1.50)
- **Required Credentials:** `OPENAI_API_KEY` (obtain from https://platform.openai.com/api-keys)
- **Fallback:** Rule-based feedback if API fails or rate limited

**Clerk Authentication:**
- **Purpose:** User authentication, OAuth2 providers, JWT management
- **Integration:** 
  - Frontend: `@clerk/clerk-react@4.27.1`
  - Backend: JWT validation via `clerk-sdk-python==0.1.2`
- **Endpoint:** https://api.clerk.dev/v1/
- **Authentication:** Secret key for backend, publishable key for frontend
- **Rate Limits:** Free tier - 5,000 MAU, Unlimited signups
- **Required Credentials:**
  - `CLERK_SECRET_KEY` - Backend API key (sk_test_...)
  - `CLERK_PUBLISHABLE_KEY` - Frontend public key (pk_test_...)
  - Obtain from https://dashboard.clerk.com
- **Features Used:** Google OAuth, GitHub OAuth, email/password, session management

### Hosting & Infrastructure

**Railway:**
- **Purpose:** Backend hosting, PostgreSQL, Redis
- **Services:**
  - FastAPI app container (512MB RAM, 1 vCPU)
  - PostgreSQL 15.4 database (500MB storage)
  - Redis 7.2 cache (100MB storage)
- **Deployment:** Git-based auto-deploy from `main` branch
- **Cost:** Free tier includes $5 monthly credits, scales to ~$10-20/month for MVP load
- **Configuration:** `railway.json` for service definitions
- **Monitoring:** Built-in metrics for CPU, memory, requests

**Vercel:**
- **Purpose:** Frontend hosting and CDN
- **Features:** Automatic HTTPS, edge caching, preview deployments per PR
- **Deployment:** Git-based auto-deploy from `main` branch
- **Cost:** Free tier - 100GB bandwidth, unlimited sites
- **Configuration:** `vercel.json` for build settings

### Development Tools

**Sentry:**
- **Purpose:** Error tracking and performance monitoring
- **Integration:** 
  - Backend: `sentry-sdk[fastapi]==1.38.0`
  - Frontend: `@sentry/react==7.85.0`
- **Cost:** Free tier - 5,000 errors/month
- **Configuration:** DSN in environment variables
- **Alerts:** Email notifications for error spikes >10/min

**Prometheus + Grafana:**
- **Purpose:** Metrics collection and visualization
- **Integration:** `prometheus-fastapi-instrumentator==6.1.0`
- **Metrics Tracked:**
  - Request rate, response time (P50, P95, P99)
  - Judge0 API latency
  - OpenAI token usage and cost
  - Database query performance
  - Cache hit rate
- **Cost:** Self-hosted on Railway (included in app container)
- **Dashboards:** Pre-configured for API performance, business metrics

### Required API Keys Summary

Create a `.env` file with the following:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/codementor_db
REDIS_URL=redis://host:6379/0

# Code Execution
JUDGE0_API_KEY=your_rapidapi_key_here
JUDGE0_API_URL=https://judge0-ce.p.rapidapi.com

# AI Feedback
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_ORG_ID=org-your_org_id (optional)

# Authentication
CLERK_SECRET_KEY=sk_test_your_clerk_secret
CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_publishable

# Monitoring
SENTRY_DSN=https://your_sentry_dsn@sentry.io/project_id

# Application
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,https://your-domain.vercel.app
```

### Rate Limits & Quotas

**Critical Limits (MVP):**
- Judge0: 50 requests/day (upgrade to paid before public beta)
- OpenAI: 500 requests/min, 200k tokens/min (sufficient for 20 concurrent users)
- Clerk: 5,000 MAU (monitor at 4,000, upgrade to Pro at $25/month)
- Railway: $5 monthly credit (~100 hours runtime, upgrade to $20/month for production)
- Vercel: 100GB bandwidth/month (monitor at 80GB)

**Cost Projections (100 daily active users):**
- Judge0: $12/month (300 submissions/day × $0.004)
- OpenAI: $15/month (~50k tokens/day × $0.30/1M)
- Railway: $20/month (continuous backend runtime)
- Clerk: $25/month (Pro plan for >5k MAU)
- **Total:** ~$72/month

---

## 15. Security Considerations

### Authentication & Authorization

**Authentication Method:**
- **Primary:** Clerk OAuth2 with JWT tokens
- **Token Lifecycle:** 
  - Access token: 1 hour expiry
  - Refresh token: 7 days expiry
  - Automatic silent refresh via Clerk SDK
- **Session Storage:** HttpOnly cookies, SameSite=Strict
- **OAuth Providers:** Google, GitHub (email/password disabled for MVP to reduce spam)

**Authorization Approach:**
- **Role-Based Access Control (RBAC):**
  - `user` role: Submit code, view own progress
  - `admin` role: View all submissions, manage problems (deferred for MVP)
- **Resource-Level Authorization:**
  - Users can only access their own submissions and progress
  - Enforce via SQLAlchemy query filters: `Submission.query.filter_by(user_id=current_user.id)`
- **JWT Validation:** 
  - Every protected endpoint validates JWT via Clerk middleware
  - Reject expired or tampered tokens

### Data Protection

**Encryption at Rest:**
- **Database:** PostgreSQL encryption enabled on Railway (AES-256)
- **Environment Variables:** Stored in Railway encrypted vault
- **Sensitive Data:** API keys never committed to Git (use `.env` with `.gitignore`)

**Encryption in Transit:**
- **TLS 1.3:** All external connections (frontend ↔ backend, backend ↔ APIs)
- **HTTPS Only:** Vercel enforces HTTPS, Railway auto-provisions SSL certs
- **API Keys in Headers:** Never in URL query parameters

**Data Minimization:**
- Only store email, user_id, and coding submissions (no PII beyond email)
- No credit card info (auth handled by Clerk)
- Submissions auto-deleted after 90 days (GDPR compliance prep)

### Key Security Risks & Mitigations

**1. Code Injection / Arbitrary Code Execution:**
- **Risk:** User submits malicious Python code to access server resources
- **Mitigation:** Judge0 sandbox with resource limits (1s CPU, 256MB RAM, no network)
- **Additional:** AST parsing rejects `import os`, `eval()`, `exec()` before submission

**2. SQL Injection:**
- **Risk:** User input in database queries
- **Mitigation:** SQLAlchemy ORM with parameterized queries (no raw SQL)
- **Validation:** Pydantic models validate all input types before queries

**3. Cross-Site Scripting (XSS):**
- **Risk:** Malicious code in problem descriptions or user submissions rendered in browser
- **Mitigation:** 
  - React auto-escapes all rendered content
  - Monaco editor sandboxes code display
  - Markdown parsing via `react-markdown` with sanitization

**4. Cross-Site Request Forgery (CSRF):**
- **Risk:** Unauthorized actions via forged requests
- **Mitigation:** 
  - SameSite=Strict cookies prevent cross-origin requests
  - JWT tokens in Authorization header (not cookies)
  - Clerk validates request origin

**5. Prompt Injection (LLM):**
- **Risk:** User submits code with instructions to manipulate GPT output
- **Mitigation:**
  - User code wrapped in delimiters: `<user_code>...</user_code>`
  - System prompt explicitly ignores instructions in user code
  - Output validation: Reject responses with suspicious patterns

**6. Denial of Service (DoS):**
- **Risk:** User floods API with requests or infinite loop submissions
- **Mitigation:**
  - Rate limiting: 20 submissions/user/hour, 10 API requests/user/min
  - Judge0 execution timeout: 1 second max
  - Circuit breaker: Block user after 5 failed submissions in 1 minute

**7. API Key Exposure:**
- **Risk:** Accidental commit of `.env` file to Git
- **Mitigation:**
  - `.gitignore` includes `.env`, `.env.local`
  - Pre-commit hooks scan for API key patterns
  - Railway/Vercel environment variables never logged

### Input Validation

**Backend (Pydantic Models):**
```python
class SubmissionCreate(BaseModel):
    problem_id: UUID
    code: str = Field(max_length=10000, min_length=1)
    language: Literal["python"] = "python"
    
    @validator('code')
    def validate_code_safety(cls, v):
        dangerous_imports = ['os', 'sys', 'subprocess', 'socket']
        for imp in dangerous_imports:
            if f'import {imp}' in v:
                raise ValueError(f'Import {imp} is not allowed')
        return v
```

**Frontend (React):**
- Monaco editor prevents submission of code >10,000 characters
- Debounced API calls to prevent rapid-fire requests

### Compliance Requirements

**For Student Project (MVP):**
- **GDPR-Ready:** User data export and deletion endpoints (not implemented until Phase 2)
- **No COPPA:** Age gate at signup (must be 13+)
- **No HIPAA/SOC2:** Not handling healthcare or financial data

**Post-MVP Considerations:**
- GDPR compliance for EU users
- CCPA compliance for California users
- Terms of Service and Privacy Policy (consult legal)

### Security Monitoring

**Automated Scanning:**
- **Dependabot:** Weekly dependency vulnerability scans
- **Snyk:** SAST (Static Application Security Testing) on PRs
- **Trivy:** Docker image vulnerability scanning

**Incident Response:**
- Sentry alerts for auth failures >10/min
- Manual review of all 5xx errors within 24 hours
- Quarterly security audit of IAM permissions

---

## 16. Performance Requirements

### Load Capacity

**MVP Targets (Week 15):**
- **Concurrent Users:** 20 simultaneous users
- **Daily Active Users:** 50 DAU
- **Code Submissions:** 100 submissions/day (~2 per user)
- **API Requests:** 500 requests/day (5× submissions for dashboard, problem list, etc.)

**Phase 2 Targets (Post-Course):**
- **Concurrent Users:** 100 simultaneous users
- **Daily Active Users:** 500 DAU
- **Code Submissions:** 1,000 submissions/day
- **API Requests:** 10,000 requests/day

### Response Time Requirements

**Critical User Flows (P95 Latency):**
1. **Code Submission → Feedback:** <10 seconds end-to-end
   - Judge0 execution: <3s
   - AST parsing: <200ms
   - Pattern detection: <500ms
   - GPT feedback generation: <5s
   - Database write: <100ms
   - Frontend rendering: <1s

2. **Problem List Load:** <2 seconds
   - Database query: <100ms
   - API response: <50ms
   - Frontend render: <1.8s (includes skeleton loader)

3. **Dashboard Load:** <3 seconds
   - Aggregate queries: <500ms (Redis cached after first load)
   - Chart rendering: <2s

4. **Authentication (Login):** <1.5 seconds
   - Clerk OAuth redirect: <1s
   - JWT validation + user fetch: <500ms

**Page Load Times:**
- **Desktop (1920x1080, Fast 3G):** <2 seconds Time to Interactive (TTI)
- **Mobile (iPhone 12, 4G):** <4 seconds TTI
- **Lighthouse Score:** >90 Performance, >95 Accessibility, >90 Best Practices

### Scalability Approach

**Horizontal Scaling:**
- **Backend:** Stateless FastAPI instances, scale to 3 containers at 80% CPU
- **Database Connection Pooling:** SQLAlchemy pool (min=5, max=20 connections)
- **Redis Caching:** 
  - Problem list: 5-minute TTL
  - User progress: 1-minute TTL
  - Repeated submissions (same code): 24-hour TTL
  - Cache invalidation on new submission

**Vertical Scaling (if needed):**
- Railway allows per-service RAM/CPU upgrades (512MB → 2GB, 1 vCPU → 2 vCPU)

**Database Optimization:**
- **Indexes:** 
  - `users.clerk_user_id` (unique)
  - `submissions.user_id, submitted_at` (composite for user history queries)
  - `problems.difficulty, tags` (composite for filtering)
  - `weakness_patterns.user_id, pattern_type` (composite for dashboard)
- **Query Optimization:** 
  - Eager loading for relationships (avoid N+1 queries)
  - Pagination: 20 problems per page, 50 submissions per page
  - `EXPLAIN ANALYZE` for slow queries >100ms

**CDN & Static Assets:**
- Vercel Edge Network caches static assets (JS, CSS, images) globally
- React code splitting: Lazy load dashboard charts (~200KB bundle)

### Resource Constraints

**Railway Free Tier Limits:**
- $5 monthly credit (~100 execution hours)
- 512MB RAM per service
- 1GB disk space
- Strategy: Upgrade to Hobby plan ($5/month per service) at 4,000 MAU

**Judge0 Free Tier:**
- 50 requests/day
- Strategy: Cache identical submissions, upgrade to paid at 40 requests/day

**OpenAI Token Budget:**
- $2/day maximum spend
- Average tokens per request: 1,500 input + 500 output = 2,000 total
- Daily capacity: ~6,600 requests (GPT-4o-mini at $0.15/1M input, $0.60/1M output)
- Strategy: Alert at $1.50/day, throttle to 90% GPT-4o-mini / 10% GPT-4o

### Performance Monitoring

**Key Metrics (Tracked in Grafana):**
- **Request Rate:** Requests per second (target: <1 RPS for MVP)
- **API Latency:** P50, P95, P99 response times (target: P95 <10s)
- **Error Rate:** 5xx errors per hour (target: <5%)
- **Database Query Time:** P95 query duration (target: <100ms)
- **Cache Hit Rate:** Redis cache hits / total requests (target: >60%)
- **Judge0 Success Rate:** Successful executions / total submissions (target: >95%)
- **OpenAI Latency:** P95 GPT response time (target: <5s)

**Performance Testing Tools:**
- **k6 Load Tests:** Weekly runs with 20 virtual users for 5 minutes
- **Lighthouse CI:** Automated on every deploy to staging
- **Backend Profiling:** `py-spy` for CPU profiling, `memory_profiler` for RAM leaks

---

## 17. Monitoring & Observability

### Logging Strategy

**Log Format:**
- **Structured JSON:** All logs output as JSON for easy parsing
- **Fields:** `timestamp`, `level`, `message`, `user_id`, `request_id`, `service`, `metadata`
- **Library:** Python `structlog` for consistent formatting

**Log Levels:**
- **ERROR:** Failed API calls, database errors, unhandled exceptions
- **WARN:** Rate limit approaching, slow queries (>500ms), fallback to cached data
- **INFO:** User actions (login, submission, problem solve), API requests
- **DEBUG:** Detailed execution flow (development only)

**Log Aggregation:**
- **Centralized:** Sentry for errors, Railway logs for info/debug
- **Retention:** 7 days for free tier, 30 days post-upgrade
- **Search:** Full-text search via Railway dashboard, Sentry issue grouping

**Example Log Entry:**
```json
{
  "timestamp": "2024-11-06T10:15:30.123Z",
  "level": "ERROR",
  "message": "Judge0 API timeout",
  "user_id": "usr_abc123",
  "request_id": "req_xyz789",
  "service": "ExecutionService",
  "metadata": {
    "problem_id": "prob_001",
    "submission_id": "sub_456",
    "error_code": "TIMEOUT",
    "duration_ms": 15000
  }
}
```

### Monitoring Tools

**Sentry (Error Tracking):**
- **Integration:** SDK in FastAPI middleware and React Error Boundary
- **Features:**
  - Automatic error capture with stack traces
  - User context (user_id, email) attached to errors
  - Breadcrumbs for action history leading to error
  - Release tracking tied to Git commits
- **Alerts:** Email on new error types, Slack webhook for critical errors

**Prometheus (Metrics Collection):**
- **Integration:** `prometheus-fastapi-instrumentator` exports `/metrics` endpoint
- **Metrics:**
  - `http_requests_total`: Counter of API requests by endpoint, method, status
  - `http_request_duration_seconds`: Histogram of response times
  - `judge0_requests_total`: Counter of Judge0 API calls
  - `openai_tokens_used`: Counter of OpenAI tokens consumed
  - `db_query_duration_seconds`: Histogram of database query times
- **Scraping:** Grafana scrapes `/metrics` every 15 seconds

**Grafana (Visualization):**
- **Dashboards:**
  1. **API Performance:** Request rate, P95 latency, error rate
  2. **Business Metrics:** Submissions/hour, unique users, problems solved
  3. **External Services:** Judge0 latency, OpenAI token usage, costs
  4. **Database Health:** Query performance, connection pool usage, cache hit rate
- **Access:** Railway-hosted Grafana instance at `https://grafana.railway.app`

**Railway Metrics (Infrastructure):**
- **Built-in:** CPU usage, memory usage, disk I/O, network traffic
- **Alerts:** Email when CPU >80% for 5 minutes or memory >90%

### Key Metrics Tracked

**User Engagement:**
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Average problems solved per user
- Submission success rate (passed tests / total submissions)
- Time spent in code editor (via frontend analytics)

**Performance:**
- API endpoint latency (P50, P95, P99)
- Database query performance
- Judge0 API response time
- OpenAI API response time
- Frontend page load times

**Reliability:**
- Error rate (5xx errors / total requests)
- Judge0 success rate
- OpenAI API failures
- Database connection errors
- Uptime percentage (target: 99.5%)

**Cost Management:**
- OpenAI daily spend (target: <$2/day)
- Judge0 request count (target: <50/day free tier)
- Railway credits consumed (alert at $4/$5)
- Total monthly infrastructure cost (target: <$75)

### Alerting Criteria

**Critical Alerts (Immediate Action):**
- Error rate >10% for 5 minutes → Email + Slack
- API latency P95 >30s for 5 minutes → Email
- Database connection pool exhausted → Email + Slack
- OpenAI daily spend >$2.00 → Email + auto-throttle
- Railway credits >80% consumed → Email

**Warning Alerts (Review within 24h):**
- Error rate >5% for 15 minutes → Email
- API latency P95 >15s for 15 minutes → Email
- Judge0 request count >40/day → Email
- Cache hit rate <50% for 1 hour → Email
- Slow queries >500ms detected → Email

**Info Alerts (Review weekly):**
- New Sentry issue types (non-critical)
- Performance regression >10% vs. previous week
- User engagement drop >20% week-over-week

---

## 18. Deployment & DevOps

### Deployment Strategy

**Continuous Deployment (CD):**
- **Frontend (Vercel):**
  - Trigger: Push to `main` branch or PR merge
  - Build: `npm run build` (Vite production build)
  - Deploy: Automatic to Vercel Edge Network (~2 minutes)
  - Rollback: One-click revert to previous deployment in Vercel dashboard

- **Backend (Railway):**
  - Trigger: Push to `main` branch
  - Build: Docker build from `Dockerfile`
  - Deploy: Zero-downtime rolling update (~3 minutes)
  - Health Check: `/health` endpoint must return 200 before traffic routing
  - Rollback: Automatic rollback if health check fails 3 times

### Environment Strategy

**Development (Local):**
- **Backend:** `http://localhost:8000`
- **Frontend:** `http://localhost:5173`
- **Database:** Local PostgreSQL or Railway dev instance
- **Redis:** Local Redis server
- **Judge0:** RapidAPI free tier (shared with staging)
- **OpenAI:** Personal API key with $5 credit limit

**Staging (Railway Preview + Vercel Preview):**
- **Backend:** `https://codementor-api-staging.railway.app`
- **Frontend:** `https://codementor-pr-<number>.vercel.app` (auto-created per PR)
- **Database:** Separate Railway database (staging_db)
- **Redis:** Shared with production (different keyspace: `staging:*`)
- **Judge0:** RapidAPI free tier (rate limit shared with dev)
- **OpenAI:** Shared production key with `staging_` prefix in logs

**Production (Railway + Vercel):**
- **Backend:** `https://api.codementor.ai` (custom domain via Railway)
- **Frontend:** `https://codementor.ai` (custom domain via Vercel)
- **Database:** Railway PostgreSQL (500MB → 5GB on upgrade)
- **Redis:** Railway Redis (dedicated instance)
- **Judge0:** Paid plan (unlimited requests)
- **OpenAI:** Production API key with $100/month budget

### CI/CD Pipeline (GitHub Actions)

**Workflow File:** `.github/workflows/ci-cd.yml`

**On Pull Request:**
```yaml
name: CI/CD Pipeline

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11.7'
      - run: pip install -r backend/requirements.txt
      - run: black --check backend/
      - run: ruff check backend/
      - run: mypy backend/
      - run: pytest backend/tests/ --cov=backend/app --cov-report=xml
      - uses: codecov/codecov-action@v3
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run type-check
      - run: cd frontend && npm test -- --coverage
  
  e2e-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    steps:
      - uses: actions/checkout@v3
      - run: docker-compose up -d
      - run: npx playwright install
      - run: npx playwright test
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
  
  deploy-staging:
    if: github.event_name == 'pull_request'
    needs: [e2e-tests]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Vercel auto-deploys PR previews"
  
  deploy-production:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: [e2e-tests]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Railway auto-deploys main branch"
      - uses: sentry-io/action-release@v1
        with:
          environment: production
          version: ${{ github.sha }}
```

**Pipeline Stages:**
1. **Lint & Format Check:** Black, Ruff, ESLint, Prettier (2 min)
2. **Type Check:** mypy for Python, TypeScript compiler (1 min)
3. **Unit Tests:** Backend (pytest) + Frontend (Jest) (5 min)
4. **Integration Tests:** API + Database tests (3 min)
5. **E2E Tests:** Playwright critical paths (10 min)
6. **Security Scan:** Snyk vulnerability check (2 min)
7. **Deploy:** Automatic if all pass (3-5 min)

**Total Pipeline Time:** ~25 minutes from PR to production

### Infrastructure as Code

**For MVP:** Not using IaC (Railway UI configuration sufficient)

**Post-MVP (Phase 2):**
- Terraform for AWS resources (self-hosted Judge0, S3 for problem assets)
- Ansible for server provisioning
- Kubernetes manifests for multi-container orchestration

### Backup & Disaster Recovery

**Database Backups:**
- **Automated:** Railway performs daily backups at 2:00 AM UTC
- **Retention:** 7 days on free tier, 30 days on paid
- **Manual:** pg_dump before major migrations
- **Storage:** Railway encrypted storage + weekly export to AWS S3 (post-MVP)

**Disaster Recovery Plan:**
1. **Database Failure:** Restore from latest Railway backup (~5 min RTO)
2. **Application Failure:** Rollback to previous deployment (~2 min RTO)
3. **Complete Railway Outage:** 
   - Migrate to Heroku using `heroku pg:push` (~30 min RTO)
   - DNS update to point to Heroku instance
4. **Data Corruption:** Restore from S3 backup + replay Redis cache (~15 min RTO)

**Recovery Time Objective (RTO):** <30 minutes
**Recovery Point Objective (RPO):** <24 hours (daily backups)

### Rollback Strategy

**Automatic Rollback Triggers:**
- Health check fails 3 consecutive times (15-second intervals)
- Error rate >20% in first 5 minutes post-deploy
- P95 latency >20s in first 5 minutes post-deploy

**Manual Rollback:**
- Railway: Click "Redeploy" on previous successful deployment
- Vercel: Select previous deployment and click "Promote to Production"
- Time to rollback: <2 minutes

**Database Migration Rollback:**
- Alembic downgrade: `alembic downgrade -1`
- Always include `downgrade()` function in migration scripts
- Test rollback in staging before production deploy

---

## 19. Future Enhancements (Post-MVP)

**Phase 2 (Weeks 16-20):**
- Multi-language support (JavaScript, Java, C++)
- Self-hosted Judge0 for <200ms latency
- Advanced pattern detection (memory leaks, recursion depth)
- Interview readiness score algorithm

**Phase 3 (Months 4-6):**
- Spaced repetition scheduling
- Video solution explanations (embedded YouTube)
- Interactive debugging with breakpoints
- Company-specific problem collections (Google, Meta, Amazon)

**Phase 4 (Months 7-12):**
- Live mock interviews with AI interviewer
- System design interview prep module
- Peer code review feature
- Mobile applications (React Native)

---

**Document Version:** 2.1
**Last Updated:** November 6, 2024
**Maintained By:** CodeMentor AI Team
**Review Cycle:** Weekly during development, monthly post-launch

---
