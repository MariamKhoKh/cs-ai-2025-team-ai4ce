# Prioritized Backlog (Version 2)

**Project Name:** CodeMentor AI  
**Last Updated:** Week 4, October 26, 2025  
**Sprint:** Week 4 of 15

---

## Backlog Overview

**Total Issues:** 28  
**P1 (Must Have):** 12 issues  
**P2 (Should Have):** 8 issues  
**P3 (Nice to Have):** 5 issues  
**Completed:** 3 issues  

**Current Sprint Focus:** Code execution sandbox integration + AST analysis foundation

---

## 🔴 Priority 1: Critical Path (Must Have for MVP)

### Issue #1: Code Execution Sandbox Integration

**Status:** 🔵 To Do  
**Assigned:** [Backend Lead]  
**Due:** Week 4 (THIS WEEK)  
**Effort:** Large (10-12 hrs)

**User Story:**
> As a user, I want to submit my code and see test results so that I know if my solution works.

**Why This Is P1:**
Without code execution, we can't validate solutions or provide feedback. This is the foundation for all analysis features. **Blocks 8 subsequent issues.**

**Acceptance Criteria:**
- [ ] Judge0 API integrated with FastAPI backend
- [ ] Code executes in <5 seconds for 95% of test cases
- [ ] Handles Python and JavaScript submissions
- [ ] Returns test results (pass/fail for each case)
- [ ] Implements timeout protection (10 second max)
- [ ] Handles runtime errors gracefully
- [ ] Security: sandboxed execution, no file system access

**Technical Requirements:**
- Use Judge0 CE (free tier: 50 requests/day) or Piston API
- Endpoint: `POST /api/execute`
- Request: `{code, language, test_cases}`
- Response: `{status, results: [{input, expected, actual, passed}], execution_time}`
- Rate limiting: 10 requests/minute per user

**Definition of Done:**
- [ ] Code committed to `feature/code-execution` branch
- [ ] Unit tests for API endpoint (mock Judge0 responses)
- [ ] Integration test: submit code → execute → return results
- [ ] Error handling tested (syntax errors, timeouts, infinite loops)
- [ ] Security validated (can't access file system)
- [ ] Code review completed
- [ ] Deployed to staging
- [ ] Documentation: `/docs/code-execution.md`

**Dependencies:**
- **Blocks:** #4 (AST Analysis), #6 (Feedback Generation), #8 (ML Model Training)
- **Blocked By:** None

**Resources:**
- Judge0 API: https://ce.judge0.com
- Piston API: https://github.com/engineer-man/piston
- Security guide: https://owasp.org/www-community/vulnerabilities/Code_Injection

---

### Issue #2: Problem Database Schema & Seed Data

**Status:** 🟡 In Progress  
**Assigned:** [Database Lead]  
**Due:** Week 4  
**Effort:** Medium (6-8 hrs)

**User Story:**
> As a user, I want to select from curated interview problems so that I can practice relevant questions.

**Why This Is P1:**
Problems are the content layer. Need at least 30 problems for meaningful testing and pattern detection.

**Acceptance Criteria:**
- [ ] PostgreSQL schema designed (problems, test_cases, tags, difficulty)
- [ ] 30 problems curated (15 arrays, 8 strings, 7 hash maps)
- [ ] Each problem has 5-10 test cases (including edge cases)
- [ ] Problems tagged with error patterns (e.g., "edge_cases_common", "complexity_trap")
- [ ] Optimal solutions documented with complexity analysis
- [ ] API endpoint: `GET /api/problems` returns list
- [ ] API endpoint: `GET /api/problems/{id}` returns problem details

**Technical Requirements:**
```sql
-- Schema
problems (id, title, description, difficulty, optimal_time_complexity, optimal_space_complexity)
test_cases (id, problem_id, input, expected_output, is_edge_case)
problem_tags (problem_id, tag_name)
optimal_solutions (problem_id, language, code, explanation)
```

**Definition of Done:**
- [ ] Migration scripts in `/migrations/`
- [ ] Seed data in `/seeds/problems.sql`
- [ ] 30 problems fully documented
- [ ] API endpoints tested
- [ ] Documentation: `/docs/problem-schema.md`

**Dependencies:**
- **Blocks:** #3 (Frontend Problem Display), #5 (User Attempts Tracking)
- **Blocked By:** None

---

### Issue #4: AST Parser & Code Analysis Engine

**Status:** 🔵 To Do  
**Assigned:** [ML Lead]  
**Due:** Week 5  
**Effort:** Large (12-14 hrs)

**User Story:**
> As a system, I need to analyze code structure to detect patterns beyond correctness.

**Why This Is P1:**
This is our core differentiator. AST analysis extracts features for ML classification and enables pattern detection.

**Acceptance Criteria:**
- [ ] Python AST parser extracts key metrics (loops, conditionals, function calls, complexity)
- [ ] Detects common patterns:
  - Nested loops (O(n²) indicator)
  - Missing edge case checks (null, empty, bounds)
  - Unused variables
  - Hardcoded values vs. generalized logic
- [ ] Compares user code structure to optimal solution
- [ ] Outputs structured analysis: `{cyclomatic_complexity, loop_depth, edge_case_checks, time_complexity_estimate}`
- [ ] Handles parse errors gracefully

**Technical Requirements:**
- Use Python `ast` module for parsing
- Feature extraction:
  - Cyclomatic complexity: count of decision points
  - Loop depth: max nesting level
  - Variable naming quality: check against common names
  - Edge case checks: look for `if len(arr) == 0`, `if n < 0`, etc.
- Endpoint: `POST /api/analyze` (receives code, returns metrics)

**Definition of Done:**
- [ ] AST parser module in `/backend/analysis/ast_parser.py`
- [ ] Unit tests with 10 example codes
- [ ] Integration test: code → parse → extract features → return metrics
- [ ] Performance: <500ms for typical submissions
- [ ] Code review completed
- [ ] Documentation: `/docs/ast-analysis.md`

**Dependencies:**
- **Blocks:** #7 (ML Model Training), #6 (Feedback Generation)
- **Blocked By:** #1 (Code Execution - need working pipeline first)

---

### Issue #5: User Attempts Tracking & Profile Storage

**Status:** 🔵 To Do  
**Assigned:** [Backend Lead]  
**Due:** Week 5  
**Effort:** Medium (6-8 hrs)

**User Story:**
> As a user, I want my practice history saved so that I can track progress over time.

**Why This Is P1:**
Pattern detection requires historical data. Can't identify "recurring mistakes" without tracking multiple attempts.

**Acceptance Criteria:**
- [ ] Database schema for user attempts and profiles
- [ ] Store every submission (code, problem_id, result, timestamp, analysis metrics)
- [ ] Calculate per-user weakness profile (error type frequency)
- [ ] API endpoint: `POST /api/attempts` (submit attempt)
- [ ] API endpoint: `GET /api/users/{id}/profile` (get weakness profile)
- [ ] Privacy: user data anonymized for ML training (opt-in)

**Technical Requirements:**
```sql
users (id, email, created_at)
attempts (id, user_id, problem_id, code, language, passed, submitted_at, analysis_json)
user_weaknesses (user_id, error_type, frequency, last_occurred, mastery_score)
```

**Definition of Done:**
- [ ] Migration scripts created
- [ ] API endpoints implemented
- [ ] Unit tests for profile calculation logic
- [ ] Integration test: submit attempt → update profile
- [ ] Documentation: `/docs/user-profile-schema.md`

**Dependencies:**
- **Blocks:** #8 (ML Model Training), #9 (Recommendation Engine), #11 (Progress Dashboard)
- **Blocked By:** #2 (Problem Database), #4 (AST Analysis)

---

### Issue #6: GPT-4 Feedback Generation

**Status:** 🔵 To Do  
**Assigned:** [AI Lead]  
**Due:** Week 6  
**Effort:** Medium (6-8 hrs)

**User Story:**
> As a user, I want clear explanations of my mistakes so that I understand how to improve.

**Why This Is P1:**
Educational feedback is the value proposition. Without explanations, we're just a test runner.

**Acceptance Criteria:**
- [ ] GPT-4o-mini integration (90% of cases)
- [ ] Prompt engineering: receives problem, user code, detected patterns, test results
- [ ] Output structured explanation:
  - What went wrong (specific to user's code)
  - Why it matters (conceptual understanding)
  - How to improve (actionable advice)
- [ ] Escalates to GPT-4o for complex cases (unclear errors, advanced patterns)
- [ ] Response time: <5 seconds for explanation generation
- [ ] Cost: <$0.012 per explanation (see cost model)

**Technical Requirements:**
- Hybrid model selection (see cost model Strategy #1)
- System prompt (compressed, 150 tokens)
- Structured output with JSON schema (see cost model Strategy #3)
- Fallback if API fails (generic template-based feedback)

**Definition of Done:**
- [ ] OpenAI API integrated
- [ ] Prompt templates created
- [ ] A/B test: 20 explanations evaluated for quality (mini vs. full)
- [ ] Cost tracking implemented
- [ ] Unit tests (mock API responses)
- [ ] Documentation: `/docs/feedback-generation.md`

**Dependencies:**
- **Blocks:** #10 (User Testing Round 1)
- **Blocked By:** #4 (AST Analysis), #1 (Code Execution)

---

### Issue #7: ML Error Pattern Classifier

**Status:** 🔵 To Do  
**Assigned:** [ML Lead]  
**Due:** Week 7  
**Effort:** Large (14-16 hrs)

**User Story:**
> As a system, I need to automatically classify error types so that I can detect patterns in user behavior.

**Why This Is P1:**
This is the intelligence layer. Without ML classification, we can't personalize recommendations or identify recurring weaknesses.

**Acceptance Criteria:**
- [ ] 500 labeled training examples collected (see data plan below)
- [ ] Feature extraction from AST metrics (complexity, loop depth, edge checks)
- [ ] Multi-label classifier trained (Random Forest or XGBoost)
- [ ] Predicts 5 error categories (start simple, expand later):
  1. Edge case omissions
  2. Suboptimal time complexity
  3. Wrong data structure choice
  4. Off-by-one errors
  5. Missing input validation
- [ ] Model accuracy: >75% on validation set
- [ ] Inference time: <200ms
- [ ] Model versioning and storage (MLflow or local pickle)

**Technical Requirements:**
- Training pipeline: `/backend/ml/train_classifier.py`
- Features: cyclomatic_complexity, loop_depth, edge_checks_count, time_complexity_ratio, test_pass_pattern
- Model: scikit-learn RandomForestClassifier (interpretable)
- Evaluation: 80/20 train/val split, cross-validation
- Endpoint: `POST /api/classify` (receives AST metrics, returns error types)

**Definition of Done:**
- [ ] Training data collected (see Issue #7a)
- [ ] Model trained and evaluated (>75% accuracy)
- [ ] Model saved to `/models/error_classifier_v1.pkl`
- [ ] API endpoint implemented
- [ ] Unit tests with sample inputs
- [ ] Performance benchmark: <200ms inference
- [ ] Documentation: `/docs/ml-classifier.md`

**Dependencies:**
- **Blocks:** #9 (Recommendation Engine), #11 (Progress Dashboard)
- **Blocked By:** #4 (AST Analysis), #5 (User Attempts), #7a (Training Data Collection)

---

### Issue #7a: ML Training Data Collection

**Status:** 🔵 To Do  
**Assigned:** [Team - All Hands]  
**Due:** Week 6  
**Effort:** Large (10-12 hrs team effort)

**User Story:**
> As a team, we need labeled training data so that our ML model can learn error patterns.

**Why This Is P1:**
No data = no ML model. This is the bottleneck for Week 7.

**Acceptance Criteria:**
- [ ] 500 labeled code submissions with error types
- [ ] Distribution:
  - 100 edge case omissions
  - 100 suboptimal complexity
  - 100 wrong data structure
  - 100 off-by-one errors
  - 100 missing validation
- [ ] Each example has: code, problem_id, error_type(s), optimal_solution
- [ ] Data stored in `/data/training_examples.json`
- [ ] Inter-rater reliability: 2 team members agree on >85% of labels

**Technical Requirements:**
**Data Sources:**
1. **GPT-4 Synthetic Generation (300 examples):**
   - Prompt: "Generate a Python solution to [problem] with [error_type]. Make it realistic."
   - Manual review for quality
2. **LeetCode Discussions (100 examples):**
   - Scrape accepted solutions with comments indicating issues
   - Manually label and anonymize
3. **Team-Generated (100 examples):**
   - Each team member solves 20 problems with intentional mistakes
   - Label own errors

**Labeling Process:**
- Use Google Sheet: Code | Problem | Error Types | Notes
- Each example reviewed by 2 people
- Discuss disagreements in team meeting

**Definition of Done:**
- [ ] 500 examples collected
- [ ] All examples labeled by 2 people
- [ ] Disagreements resolved
- [ ] Data formatted as JSON
- [ ] Data quality report: `/docs/training-data-report.md`

**Dependencies:**
- **Blocks:** #7 (ML Model Training)
- **Blocked By:** #2 (Problem Database - need problems to generate examples for)

---

### Issue #3: Frontend Problem Display & Code Editor

**Status:** 🔵 To Do  
**Assigned:** [Frontend Lead]  
**Due:** Week 5  
**Effort:** Medium (8-10 hrs)

**User Story:**
> As a user, I want to browse problems and write code in a comfortable editor.

**Why This Is P1:**
Users need a way to interact with the system. This is the UI foundation.

**Acceptance Criteria:**
- [ ] Problem list page displays 30 problems (title, difficulty, tags)
- [ ] Problem detail page shows description, examples, constraints
- [ ] Monaco Editor integrated (VS Code's editor)
- [ ] Language selection (Python, JavaScript)
- [ ] "Submit" button calls backend API
- [ ] Test results displayed after submission (pass/fail per case)
- [ ] Syntax highlighting and auto-complete working

**Technical Requirements:**
- React + TypeScript
- Monaco Editor component: `@monaco-editor/react`
- API integration: `/api/problems`, `/api/execute`
- Responsive design (works on laptop, no mobile needed for MVP)

**Definition of Done:**
- [ ] Components created: `ProblemList.tsx`, `ProblemDetail.tsx`, `CodeEditor.tsx`
- [ ] Unit tests for components
- [ ] Integration test: select problem → write code → submit → see results
- [ ] UI reviewed by team (usability check)
- [ ] Deployed to staging (Vercel)

**Dependencies:**
- **Blocks:** #10 (User Testing Round 1)
- **Blocked By:** #2 (Problem Database), #1 (Code Execution)

---

### Issue #9: Personalized Recommendation Engine

**Status:** 🔵 To Do  
**Assigned:** [ML Lead]  
**Due:** Week 10  
**Effort:** Large (10-12 hrs)

**User Story:**
> As a user, I want problem recommendations tailored to my weaknesses so that I improve efficiently.

**Why This Is P1:**
This is the killer feature. Random practice is the baseline; personalized queuing is our innovation.

**Acceptance Criteria:**
- [ ] Algorithm calculates mastery score (0-100) per error type
- [ ] Identifies bottom 2 weaknesses for each user
- [ ] Retrieves problems tagged with those weaknesses
- [ ] Filters by appropriate difficulty (adaptive based on performance)
- [ ] Avoids recently attempted problems (within last 10)
- [ ] 10% exploration (random problems to prevent filter bubble)
- [ ] Recommendation refreshes after each attempt
- [ ] API endpoint: `GET /api/recommendations/{user_id}` returns next 3 problems

**Technical Requirements:**
```python
def recommend_problems(user_id):
    profile = get_user_weaknesses(user_id)
    target_weaknesses = bottom_k(profile.mastery_scores, k=2)
    
    candidates = get_problems_by_tags(target_weaknesses)
    candidates = filter_by_difficulty(candidates, user_adaptive_level)
    candidates = exclude_recent(candidates, user_id, last_n=10)
    
    if random() < 0.1:  # Exploration
        return random.choice(all_problems)
    else:  # Exploitation
        return top_k(candidates, k=3, score_fn=relevance_score)
```

**Definition of Done:**
- [ ] Recommendation algorithm implemented
- [ ] Unit tests with mock user profiles
- [ ] Integration test: user submits code → profile updates → recommendations refresh
- [ ] A/B test plan: personalized vs. random (for Week 12 user testing)
- [ ] Documentation: `/docs/recommendation-algorithm.md`

**Dependencies:**
- **Blocks:** #10 (User Testing Round 1), #11 (Progress Dashboard)
- **Blocked By:** #7 (ML Classifier), #5 (User Attempts)

---

### Issue #10: User Testing Round 1 (Core Flow)

**Status:** 🔵 To Do  
**Assigned:** [All Team]  
**Due:** Week 8  
**Effort:** Medium (6-8 hrs prep + testing)

**User Story:**
> As a team, we need to validate core functionality works before building advanced features.

**Why This Is P1:**
Early testing prevents building on a broken foundation. Need feedback before Week 10.

**Acceptance Criteria:**
- [ ] 5 users recruited (CS students, junior/senior)
- [ ] 45-minute testing sessions scheduled
- [ ] Test protocol created (see proposal Section 7)
- [ ] Users complete 2 problems end-to-end
- [ ] Feedback collected on:
  - Code editor usability
  - Explanation clarity
  - Error detection accuracy
  - Overall flow
- [ ] SUS score measured (target: >70)
- [ ] Critical bugs identified and prioritized

**Technical Requirements:**
- IRB consent form (adapted from course template)
- Screen recording setup (with permission)
- Survey: SUS + custom questions
- Data: anonymized feedback in `/research/round1-feedback.md`

**Definition of Done:**
- [ ] 5 users tested
- [ ] Feedback documented
- [ ] Bug list created (Issues #14-18)
- [ ] Summary report: `/research/user-testing-round1.md`
- [ ] Team retrospective meeting held

**Dependencies:**
- **Blocks:** #12 (User Testing Round 2)
- **Blocked By:** #3 (Frontend), #6 (Feedback), #9 (Recommendations)

---

### Issue #11: Progress Dashboard (Mastery Visualization)

**Status:** 🔵 To Do  
**Assigned:** [Frontend Lead]  
**Due:** Week 11  
**Effort:** Medium (8-10 hrs)

**User Story:**
> As a user, I want to see my improvement over time so that I stay motivated.

**Why This Is P1:**
Progress visibility drives engagement. Users need to see they're improving.

**Acceptance Criteria:**
- [ ] Dashboard page displays:
  - Mastery scores by error type (bar chart)
  - Problems solved over time (line chart)
  - Streak calendar (GitHub-style)
  - Top 3 weaknesses highlighted
  - "Interview Ready" score (0-100)
- [ ] Charts update in real-time after submissions
- [ ] Mobile-responsive design

**Technical Requirements:**
- Recharts library for visualizations
- API endpoint: `GET /api/users/{id}/stats`
- Data aggregation in backend (calculate mastery scores, streak)

**Definition of Done:**
- [ ] Dashboard component created
- [ ] API integration tested
- [ ] Charts render correctly with sample data
- [ ] UI reviewed by team
- [ ] Deployed to staging

**Dependencies:**
- **Blocks:** #12 (User Testing Round 2)
- **Blocked By:** #5 (User Attempts), #7 (ML Classifier)

---

### Issue #12: User Testing Round 2 (Longitudinal Study)

**Status:** 🔵 To Do  
**Assigned:** [All Team]  
**Due:** Week 12  
**Effort:** Large (12+ hrs over 2 weeks)

**User Story:**
> As a team, we need to validate that users actually improve with our platform.

**Why This Is P1:**
This is our evidence for the final demo. Need data showing measurable improvement.

**Acceptance Criteria:**
- [ ] 8 users recruited (can include 3 from Round 1)
- [ ] Users practice for 2 weeks (5+ problems minimum)
- [ ] Pre/post surveys measure confidence
- [ ] Track metrics:
  - Error pattern frequency (should decrease)
  - Time to solve (should decrease)
  - First-attempt success rate (should increase)
- [ ] Exit interviews (30 min each)
- [ ] A/B test: personalized recs vs. random (4 users each)

**Definition of Done:**
- [ ] 8 users completed 2-week study
- [ ] Pre/post data collected
- [ ] Statistical analysis: t-test for improvement (p < 0.05)
- [ ] A/B test results: personalized outperforms random
- [ ] Report: `/research/user-testing-round2.md`
- [ ] Quotes and testimonials collected for demo

**Dependencies:**
- **Blocks:** Final Demo (Week 15)
- **Blocked By:** #10 (Round 1), #11 (Dashboard), #9 (Recommendations)

---

## 🟡 Priority 2: Enhanced Features (Should Have)

### Issue #13: Multi-Language Support (JavaScript)

**Status:** 🔵 To Do  
**Assigned:** [Backend Lead]  
**Due:** Week 9  
**Effort:** Medium (6-8 hrs)

**User Story:**
> As a user preparing for JavaScript roles, I want to practice in JavaScript.

**Why This Is P2:**
Expands user base but not critical for MVP (can demo with Python only).

**Acceptance Criteria:**
- [ ] JavaScript AST parser (using Acorn library)
- [ ] JavaScript code execution via Judge0
- [ ] Same error patterns detected as Python
- [ ] 10 problems have JavaScript starter code

**Dependencies:**
- **Blocked By:** #4 (AST Analysis - Python first)

---

### Issue #14: Code Quality Feedback (Beyond Correctness)

**Status:** 🔵 To Do  
**Assigned:** [ML Lead]  
**Due:** Week 9  
**Effort:** Small (4-6 hrs)

**User Story:**
> As a user, I want feedback on code style and readability, not just correctness.

**Why This Is P2:**
Interviews care about clean code, but functionality is higher priority.

**Acceptance Criteria:**
- [ ] Detect poor variable names (e.g., `x`, `temp`, `data`)
- [ ] Detect missing comments for complex logic
- [ ] Detect overly long functions (>50 lines)
- [ ] Feedback shown as "bonus tip" section

---

### Issue #15: Email Notifications (Practice Reminders)

**Status:** 🔵 To Do  
**Due:** Week 10  
**Effort:** Small (3-4 hrs)

**User Story:**
> As a user, I want reminders to practice so that I build consistency.

**Why This Is P2:**
Engagement boost but not required for core functionality.

**Acceptance Criteria:**
- [ ] Daily email: "Your next recommended problem"
- [ ] Weekly summary: "You solved X problems this week"
- [ ] Unsubscribe option

---

### Issue #16: Problem Difficulty Calibration

**Status:** 🔵 To Do  
**Due:** Week 10  
**Effort:** Medium (6 hrs)

**User Story:**
> As a user, I want problems matched to my skill level so that I'm challenged but not overwhelmed.

**Why This Is P2:**
Nice for UX but manual difficulty tags sufficient for MVP.

**Acceptance Criteria:**
- [ ] Adaptive difficulty: if user struggling (>3 attempts), suggest easier variant
- [ ] If user breezing through (1-attempt solves), increase difficulty
- [ ] Target: 70% success rate

---

### Issue #17: Hint System

**Status:** 🔵 To Do  
**Due:** Week 11  
**Effort:** Small (4 hrs)

**User Story:**
> As a user stuck on a problem, I want progressive hints so that I can make progress without seeing the full solution.

**Why This Is P2:**
Helpful but not essential (users can see explanation after failing).

**Acceptance Criteria:**
- [ ] "Get Hint" button
- [ ] 3-level hints: approach → data structure → pseudocode
- [ ] GPT-4o-mini generates hints (low cost)

---

### Issue #18: Social Features (Leaderboard)

**Status:** 🔵 To Do  
**Due:** Week 12  
**Effort:** Small (3-4 hrs)

**User Story:**
> As a competitive user, I want to see how I rank against peers.

**Why This Is P2:**
Gamification boost but adds complexity (privacy concerns).

**Acceptance Criteria:**
- [ ] Anonymous leaderboard (username only)
- [ ] Ranked by: problems solved, mastery score
- [ ] Opt-in only

---

### Issue #19: Export Progress Report (PDF)

**Status:** 🔵 To Do  
**Due:** Week 13  
**Effort:** Small (4 hrs)

**User Story:**
> As a user, I want to download my progress report to show recruiters.

**Why This Is P2:**
Nice professional touch but not MVP.

---

### Issue #20: Video Solution Walkthroughs

**Status:** 🔵 To Do  
**Due:** Week 13  
**Effort:** Large (requires content creation)

**User Story:**
> As a visual learner, I want video explanations of optimal solutions.

**Why This Is P2:**
High value but massive time investment (defer to post-course).

---

## 🟢 Priority 3: Nice-to-Have (Could Have)

### Issue #21: Mobile App

**Why P3:** Out of scope for 15-week capstone. Web-first approach sufficient.

---

### Issue #22: Live Mock Interviews

**Why P3:** Requires real-time video infrastructure (complex). Post-course feature.

---

### Issue #23: Company-Specific Problem Sets

**Why P3:** Requires partnership with companies (not feasible in timeframe).

---

### Issue #24: Collaborative Coding (Pair Programming Mode)

**Why P3:** WebRTC complexity too high for MVP.

---

### Issue #25: Advanced Analytics (Time Complexity Heatmaps)

**Why P3:** Cool visualization but not critical for user value.

---

## 🚫 Rejected / Cut Features

- **System Design Interviews:** Cut because coding problems are complex enough. System design requires different skill set and content.
- **Behavioral Interview Questions:** Cut because AI can't assess soft skills effectively. Out of scope.
- **Integration with Company ATSs:** Cut because no partnerships available. Post-course monetization feature.
- **Custom Problem Upload:** Cut because curation is our value-add. User-generated problems add moderation complexity.

---

## 📅 Sprint Timeline

### Week 4 (Current)
- [ ] #1: Code Execution Sandbox (P1 - CRITICAL)
- [ ] #2: Problem Database (P1 - In Progress)

### Week 5
- [ ] #4: AST Parser (P1)
- [ ] #5: User Attempts Tracking (P1)
- [ ] #3: Frontend Problem Display (P1)

### Week 6
- [ ] #7a: Training Data Collection (P1 - ALL HANDS)
- [ ] #6: GPT-4 Feedback (P1)

### Week 7
- [ ] #7: ML Classifier (P1)

### Week 8
- [ ] #10: User Testing Round 1 (P1)
- [ ] Bug fixes from testing

### Week 9
- [ ] #13: JavaScript Support (P2)
- [ ] #14: Code Quality Feedback (P2)

### Week 10
- [ ] #9: Recommendation Engine (P1 - CRITICAL)
- [ ] #15: Email Notifications (P2)
- [ ] #16: Difficulty Calibration (P2)

### Week 11
- [ ] #11: Progress Dashboard (P1)
- [ ] #17: Hint System (P2)

### Week 12
- [ ] #12: User Testing Round 2 (P1 - CRITICAL)
- [ ] #18: Leaderboard (P2)

### Week 13
- [ ] Bug fixes and polish
- [ ] #19: Export Report (P2)

### Week 14
- [ ] Final polish
- [ ] Demo preparation
- [ ] Video recording

### Week 15
- [ ] **Final Demo & Presentation**

---

**Critical Path Dependencies:**
```
#1 (Execution) → #4 (AST) → #7 (ML) → #9 (Recommendations) → #10 (Testing)
                           ↓
                     #6 (Feedback)
```

**Document Version:** 2.0  
**Last Updated:** October 26, 2025  
**Next Review:** Week 6 (after user testing prep)