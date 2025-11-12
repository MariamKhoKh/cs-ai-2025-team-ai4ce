# Safety and Privacy Checklist
**Lab 6: Function Calling & Structured Outputs**  
**Project:** CodeMentor AI  
**Team:** AI4ce

| Check | Status |
|-------|---------|
| Removed all API keys from code | ✅ |
| No private or personal data used | ✅ |
| Function handles bad inputs safely | ✅ |
| Function returns friendly error messages | ✅ |
| User consent not required (no user data collected) | ✅ |

---

## API Key Security

**Status:** ✅ All keys stored in `.env` file

- Gemini API key loaded using `python-dotenv` in `agent.py`
- `.env` added to `.gitignore` 
- Verified no keys in commit history with `git log -p | grep -i "key"`
- Team members use `.env.example` as template

**Evidence from our code:**
```python
# ✅ Correct (using environment variable)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ❌ Never did this (no hardcoded keys)
# genai.configure(api_key="AIza...")
```

---

## Data Privacy

**Status:** ✅ Using mock data only

Current implementation in `tools.py`:
- User IDs are fake placeholders ("user_001", "user_002")
- Problem data hardcoded in `MOCK_PROBLEMS` dictionary
- User weaknesses stored in `USER_WEAKNESS_PROFILES` (mock data)
- Code submissions processed in memory only (not persisted)
- No real student data collected

**Future considerations (Week 7+):**
- Will add proper authentication before storing real submissions
- Plan to use parameterized SQL queries to prevent injection
- Will implement data retention policy for PostgreSQL database

---

## Input Validation

**Status:** ✅ Pydantic models validate all inputs

All three functions use Pydantic models defined in `function_models.py`:

```python
class CodeSubmissionRequest(BaseModel):
    problem_id: str = Field(description="Problem ID")
    user_code: str = Field(description="User's submitted code")
    language: Literal["python", "javascript"]  # Restricted choices
    user_id: str = Field(default="user_001")
```

**Validation rules we implemented:**
- `language` field restricted to only "python" or "javascript"
- `problem_id` must be a string (checked against MOCK_PROBLEMS)
- Error patterns use `Literal` type with 13 specific categories
- Difficulty levels restricted to "easy", "medium", "hard"

**What happens with bad inputs:**
- Invalid problem ID → Returns CodeAnalysisResponse with error message
- Wrong language → Pydantic raises ValidationError
- Missing required fields → Pydantic prevents function execution

---

## Example Safety Handling

If a user submits invalid data or a function fails, our error handling catches it:

**Example 1: Invalid problem ID**
```python
analyze_code_submission(problem_id="fake-problem", user_code="def solve(): pass", language="python")
→ Returns: CodeAnalysisResponse with test_results=[TestResult with error_message="Problem not found"]
```

**Example 2: Invalid language**
```python
analyze_code_submission(problem_id="two-sum", user_code="code", language="ruby")
→ Pydantic ValidationError: "Input should be 'python' or 'javascript'"
```

**Example 3: Function execution error**
All three functions wrapped in try-except blocks in `tools.py`:
```python
try:
    # Function logic
    return CodeAnalysisResponse(...)
except Exception as e:
    return CodeAnalysisResponse(
        submission_id=f"sub_error_{uuid.uuid4().hex[:8]}",
        ai_feedback=f"Error analyzing code: {str(e)}",
        all_tests_passed=False,
        ...
    )
```

Our error responses are user-friendly and never expose internal details.

---

## Plan to Improve

**Week 7 (Code Execution):**
- Add Judge0 API sandboxing for safe code execution
- Implement timeouts (5 seconds max per execution)
- Set memory limits (256MB) to prevent resource exhaustion
- Block network and file system access in execution environment

**Week 8 (Content Safety):**
- Add profanity filter to check user code comments
- Implement rate limiting (max 10 submissions per minute per user)
- Monitor AI feedback responses for inappropriate content

**Week 9 (Production):**
- Add logging for security events (failed validations, suspicious patterns)
- Set up monitoring alerts for unusual activity
- Implement HTTPS-only in production deployment
