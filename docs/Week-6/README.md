# CodeMentor AI - Week 6 Implementation

**Course:** Building AI-Powered Applications  
**Team:** AI4ce  
**Project:** CodeMentor AI(Technical Interview Prep with Personalized Weakness Detection)

---

## Week 6 Overview

This week implements **function calling** and **structured outputs** for the CodeMentor AI capstone project. The AI can now take real actions: analyze code, recommend problems, and track progress.

---

## Implemented Functions

### 1. `analyze_code_submission()`

**Purpose:** Analyze user's submitted code, run tests, detect error patterns, and provide AI-generated feedback.

**Input:**
- `problem_id` (str): Problem identifier (e.g., "two-sum")
- `user_code` (str): User's submitted code
- `language` (str): Programming language ("python" or "javascript")
- `user_id` (str, optional): User identifier (default: "user_001")

**Output (CodeAnalysisResponse):**
```python
{
    "submission_id": "sub_abc123",
    "problem_id": "two-sum",
    "test_results": [
        {
            "test_name": "Test 1",
            "passed": true,
            "expected": "[0,1]",
            "actual": "[0,1]"
        }
    ],
    "all_tests_passed": true,
    "detected_patterns": [
        {
            "pattern_type": "edge_case_missing",
            "severity": "high",
            "description": "Code doesn't check for empty inputs"
        }
    ],
    "ai_feedback": "Great job! Your solution passes...",
    "time_complexity": "O(n²)",
    "space_complexity": "O(n)",
    "execution_time_ms": 45.2,
    "timestamp": "2025-11-11T10:30:00"
}
```

**Use Case:** When a user submits code for a problem, this function validates correctness, identifies coding weaknesses, and provides personalized feedback.

---

### 2. `get_recommended_problem()`

**Purpose:** Recommend the next problem based on user's weakness profile.

**Input:**
- `user_id` (str, optional): User identifier (default: "user_001")
- `difficulty_level` (str, optional): Desired difficulty ("easy", "medium", "hard")

**Output (RecommendationResponse):**
```python
{
    "recommended_problem": {
        "problem_id": "valid-parentheses",
        "title": "Valid Parentheses",
        "description": "Given a string containing...",
        "difficulty": "medium",
        "target_patterns": ["edge_case_missing"],
        "estimated_time_minutes": 30
    },
    "recommendation_reason": "This problem targets your weakest area: edge case missing. Your current mastery: 45/100",
    "user_weakness_areas": ["edge_case_missing", "suboptimal_time_complexity", "wrong_data_structure"]
}
```

**Use Case:** After completing a problem (or on app launch), suggest what the user should practice next to improve their weakest areas.

---

### 3. `track_user_progress()`

**Purpose:** Update user's weakness profile after each submission to track improvement over time.

**Input:**
- `user_id` (str): User identifier
- `problem_id` (str): Problem that was attempted
- `detected_patterns` (List[str]): Error patterns found in submission
- `time_taken_minutes` (float): Time spent on problem
- `attempts_count` (int): Number of attempts made
- `solved_correctly` (bool): Whether problem was solved

**Output (ProgressTrackingResponse):**
```python
{
    "user_id": "user_001",
    "updated_weaknesses": [
        {
            "pattern_type": "edge_case_missing",
            "mastery_score": 42.0,
            "trend": "declining",
            "problems_attempted": 10
        },
        {
            "pattern_type": "off_by_one",
            "mastery_score": 73.0,
            "trend": "improving",
            "problems_attempted": 8
        }
    ],
    "overall_mastery": 58.3,
    "next_focus_area": "edge_case_missing",
    "problems_solved_total": 25,
    "streak_days": 3,
    "timestamp": "2025-11-11T10:35:00"
}
```

**Use Case:** After code analysis, update the user's profile so future recommendations are more personalized and the dashboard shows progress trends.

## Setup Instructions

### 1. Install Dependencies

```bash
requirements.txt
```

### 2. Configure API Key

```bash
# Copy example file
cp .env.example .env

# Edit .env and add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

### 3. Run Tests

```bash
# Run all tests
pytest tests/test_functions.py -v

# Run specific test
pytest tests/test_functions.py::test_analyze_code_basic -v
```

### 4. Try the Agent

```python
from src.ai.agent import CodeMentorAgent

agent = CodeMentorAgent()
agent.start_conversation()

response = agent.send_message("What problem should I practice next?")
print(response)
```

---

## Test Results Summary

**Total Tests:** 17  
**Passed:** 17   
**Failed:** 0   

**Coverage:**
- `analyze_code_submission`: 5 tests
- `get_recommended_problem`: 4 tests  
- `track_user_progress`: 5 tests
- Integration & Performance: 3 tests

**Average Latencies:**
- `analyze_code_submission`: ~45ms
- `get_recommended_problem`: ~12ms
- `track_user_progress`: ~8ms

See `docs/evaluation_notes.md` for detailed metrics.

---

## Security & Safety

- No API keys in code (uses environment variables)
- All functions have error handling with fallbacks
- Input validation via Pydantic models
- Mock data for Week 6 (no real user data exposed)
- `.env` file in `.gitignore`

See `course-pack/labs/lab-6/safety_checklist.md` for full details.

---

## Technology Stack

- **Language:** Python 3.11
- **LLM:** Google Gemini 1.5 Flash
- **Validation:** Pydantic v2
- **Testing:** pytest
- **Code Execution (future):** Judge0 API
- **Database (future):** PostgreSQL

---

## 📈Next Steps (Week 7+)

1. **Replace mock data** with real code execution (Judge0 integration)
2. **Add database** for persistent user profiles (PostgreSQL)
3. **Build frontend** code editor (React + Monaco Editor)
4. **Train ML classifier** for error pattern detection
5. **Implement collaborative filtering** for better recommendations

---

## Team

**AI4ce Team**
- Focus: Technical interview preparation with AI-powered weakness detection
- Goal: Help candidates identify and fix blind spots before real interviews

---

## License

Educational project for Building AI-Powered Applications course.

---

## Links

- [Demo Video](#) *(Add your YouTube/Drive link here)*
