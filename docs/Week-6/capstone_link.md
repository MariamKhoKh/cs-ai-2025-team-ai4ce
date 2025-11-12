# Capstone Link
**Team Name:** AI4ce  
**Project Title:** CodeMentor AI - Technical Interview Prep with Personalized Weakness Detection  
**Date:** November 11, 2025

---

## Function Reused from Lab 6

**`analyze_code_submission(problem_id, user_code, language, user_id)`**

**Purpose:** Analyzes user's code submission to detect error patterns, run test cases, estimate complexity, and provide AI-generated feedback

**Why this function is critical:**  
This is the core intelligence of CodeMentor AI. Without it, the capstone would just be a static problem bank. With it, the AI can understand what the user struggles with and provide personalized feedback. This function is the entry point for our entire workflow:

1. Takes in user code (input from Monaco editor)
2. Runs test cases via `_run_mock_tests()` (will be Judge0 in Week 7)
3. Detects patterns using `_detect_error_patterns()` (checks for edge cases, nested loops, wrong data structures)
4. Estimates complexity via `_estimate_complexity()` (O(n), O(n²), etc.)
5. Returns structured `CodeAnalysisResponse` with all results
6. Feeds detected patterns into `track_user_progress()` to update mastery scores

---

## Integration Plan

### Week 7: Real Code Execution
**Current state:** Using mock test results in `_run_mock_tests()`  
**Next step:** Integrate Judge0 API for actual code execution

**Tasks:**
1. ✅ Functions already in `src/backend/functions/tools.py`
2. ⬜ Sign up for Judge0 RapidAPI and get credentials
3. ⬜ Create `judge0_client.py` helper module
4. ⬜ Replace `_run_mock_tests()` with Judge0 submission API calls
5. ⬜ Add timeout handling (5 seconds max execution time)
6. ⬜ Parse Judge0 response JSON and convert to our `TestResult` format
7. ⬜ Update `analyze_code_submission()` to use real execution

**Example flow:**
```python
# Current (Week 6):
test_results = _run_mock_tests(problem_id, user_code)

# Week 7:
submission_token = judge0_submit(user_code, problem_id)
judge0_result = judge0_get_result(submission_token)
test_results = parse_judge0_response(judge0_result)
```

**Risk:** Judge0 might be slow (>2 seconds per submission). Backup plan: self-host Judge0 using Docker Compose on AWS EC2.

---

### Week 8: Database Integration
**Current state:** All data in memory (`MOCK_PROBLEMS`, `USER_WEAKNESS_PROFILES`)  
**Next step:** Persist submissions and user profiles to PostgreSQL

**Tasks:**
1. ⬜ Create database schema:
   - `submissions` table: id, user_id, problem_id, code, detected_patterns, timestamp, passed
   - `user_profiles` table: user_id, weakness_scores (JSONB), overall_mastery, last_updated
   - `problems` table: problem_id, title, description, difficulty, test_cases (JSONB)
2. ⬜ Write SQLAlchemy models for all three tables
3. ⬜ Update `analyze_code_submission()` to INSERT each submission after analysis
4. ⬜ Update `track_user_progress()` to UPDATE user_profiles table
5. ⬜ Update `get_recommended_problem()` to SELECT from problems table
6. ⬜ Add migration script to load MOCK_PROBLEMS into database

**Example query:**
```sql
INSERT INTO submissions (user_id, problem_id, code, detected_patterns, passed, timestamp)
VALUES (%s, %s, %s, %s, %s, NOW());

UPDATE user_profiles 
SET weakness_scores = %s, overall_mastery = %s, last_updated = NOW()
WHERE user_id = %s;
```

---

### Week 9: Frontend Integration
**Current state:** Functions work via API calls in backend, tested in `agent.py`  
**Next step:** Build React frontend with code editor

**Tasks:**
1. ⬜ Install Monaco Editor React package (`@monaco-editor/react`)
2. ⬜ Create `CodeSubmissionForm` component with editor and submit button
3. ⬜ Create API endpoint: `POST /api/analyze` that calls `analyze_code_submission()`
4. ⬜ Display test results in `TestResultsPanel` component
5. ⬜ Display AI feedback in `FeedbackPanel` with syntax highlighting
6. ⬜ Add loading spinner while Judge0 processes submission
7. ⬜ Create `ProgressDashboard` that shows mastery scores from `track_user_progress()`

**User experience:**
```
1. User opens problem "Two Sum" → Monaco editor loads with problem description
2. User types solution → Syntax highlighting shows in real-time
3. User clicks "Submit" → Loading spinner appears
4. Frontend calls POST /api/analyze → Backend calls analyze_code_submission()
5. Results appear: 3/5 tests passed ✅✅✅❌❌
6. Feedback panel shows: "Missing edge case: empty array input"
7. Complexity shown: Time: O(n²), Space: O(1)
```

---

## How Lab 6 Functions Work Together

The three functions work as a continuous learning loop:

**Flow:**
```
1. analyze_code_submission(problem_id, user_code, language)
   ↓ Returns: CodeAnalysisResponse with detected_patterns
   
2. track_user_progress(user_id, problem_id, detected_patterns, ...)
   ↓ Updates mastery scores, Returns: ProgressTrackingResponse with next_focus_area
   
3. get_recommended_problem(user_id, difficulty_level)
   ↓ Uses mastery scores to find weakest area
   ↓ Returns: RecommendationResponse with problem targeting weakness
   
4. User solves recommended problem → Loop back to step 1
```

**Example from our tests:**
```python
# Step 1: User submits code with nested loops
analysis = analyze_code_submission(
    problem_id="two-sum",
    user_code="for i in range(n): for j in range(n): ...",
    language="python"
)
# Returns: detected_patterns=["suboptimal_time_complexity"]

# Step 2: Track progress
progress = track_user_progress(
    user_id="user_001",
    problem_id="two-sum",
    detected_patterns=["suboptimal_time_complexity"],
    time_taken_minutes=12.0,
    attempts_count=2,
    solved_correctly=False
)
# Updates: suboptimal_time_complexity mastery: 60 → 55

# Step 3: Get recommendation
recommendation = get_recommended_problem(
    user_id="user_001",
    difficulty_level="easy"
)
# Returns: Problem targeting "suboptimal_time_complexity" (lowest score)
```

---

## Next Step (This Week)

**Priority 1:** Get Judge0 working with `analyze_code_submission()`  
**Assigned to:** Backend team  
**Deadline:** End of Week 7

**Specific sub-tasks:**
1. ✅ Research Judge0 API documentation and pricing
2. ⬜ Create RapidAPI account and get Judge0 API key
3. ⬜ Write `judge0_client.py` helper module with:
   - `submit_code(source_code, language_id, stdin, expected_output)` → returns token
   - `get_submission(token)` → returns result with status, stdout, stderr, time, memory
4. ⬜ Update `_run_mock_tests()` to use Judge0 instead of mock logic
5. ⬜ Add error handling for Judge0 timeouts and failures
6. ⬜ Test with all three MOCK_PROBLEMS to verify results match expected format
7. ⬜ Update tests in `test_tools.py` to handle real execution times

**Success criteria:** 
- By end of Week 7, we can submit actual Python code
- Code executes in Judge0 sandbox
- Get real pass/fail results (not mocked)
- Response still returns proper `CodeAnalysisResponse` format
- All tests pass with real execution

---

## Why This Matters for Capstone

**Without Lab 6 functions:**
- Static problem list with no personalization
- No way to track if user is improving over time
- Manual feedback from instructor (doesn't scale)
- Users don't know what to practice next

**With Lab 6 functions:**
- AI automatically detects what user struggles with (13 pattern types)
- Adaptive recommendations based on weakness areas (targets lowest mastery scores)
- Personalized feedback on every submission (AI-generated)
- Data-driven progress tracking (mastery scores update after each submission)
- Users see clear improvement metrics (overall_mastery, streak_days, problems_solved_total)

This transforms the capstone from a simple coding problem website into an intelligent tutoring system that learns from each user's mistakes and adapts to help them improve.

**Real-world impact:**
- Students preparing for FAANG interviews get personalized practice
- Identifies blind spots users don't notice themselves (e.g., always forgetting edge cases)
- Saves time by focusing on weaknesses instead of random practice
- Builds confidence through measurable progress (mastery scores)

---

## Long-term Vision (Week 12 Demo)

By final demo, `analyze_code_submission()` should:

**Core Features:**
- ✅ Execute real code in sandboxed environment (Judge0 API)
- ✅ Detect 13+ error pattern types (edge cases, complexity, data structures)
- ✅ Store all submissions in PostgreSQL database
- ✅ Return feedback in < 3 seconds (including Judge0 execution)
- ✅ Integrate with Monaco editor in React frontend
- ✅ Support Python and JavaScript submissions

**Advanced Features (if time permits):**
- ⬜ ML-powered pattern detection instead of rule-based (train classifier on 500+ submissions)
- ⬜ Progressive hints system (uses detected patterns to give targeted hints without spoiling solution)
- ⬜ Compare user's solution to optimal solution (side-by-side diff view)
- ⬜ Leetcode-style runtime percentile ("Your solution is faster than 85% of submissions")

**Success Metrics:**
- **Accuracy:** Pattern detection ≥80% precision (manual labeling validation)
- **Speed:** End-to-end response < 3 seconds
- **Usefulness:** ≥70% of beta testers say feedback helped them improve (user survey)
- **Reliability:** Handle 50 concurrent submissions without crashing (load testing with Apache Bench)
