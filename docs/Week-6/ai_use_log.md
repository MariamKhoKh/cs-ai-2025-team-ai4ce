# AI Tool Use Log
**Lab 6: Function Calling & Structured Outputs**  
**Project:** CodeMentor AI  
**Team:** AI4ce

| Tool | Used For | Description |
|------|-----------|--------------|
| Claude (Anthropic) | Pydantic model structure | Asked: "How do we create Pydantic models with Field validation and Literal types for code analysis?" Generated base structure for CodeAnalysisResponse, RecommendationResponse, ProgressTrackingResponse |
| Claude | Function implementation | Asked: "Write Python functions that return Pydantic models for code analysis, problem recommendation, and progress tracking." Generated skeletons with docstrings |
| Claude | Test case generation | Asked: "Write pytest tests for analyze_code_submission that check edge cases, error handling, and performance." Generated initial test structure |
| Claude | Debugging | Helped fix import errors and function signature mismatches during testing |
| GitHub Copilot | Auto-completion | Auto-suggested import statements, type hints (List[ErrorPattern]), and completed dictionary structures for MOCK_PROBLEMS |
| ChatGPT | Research | Asked: "What are common error patterns in technical interview coding?" and "How to structure function declarations for Gemini API?" |
| ChatGPT | Best practices | Asked: "Best practices for testing AI-powered functions with mock data?" Got general guidance on test organization |

---

## Detailed Usage

### 1. Pydantic Models (Claude)

**What we asked:** "Create Pydantic models for three functions: code analysis that returns test results and detected patterns, problem recommendation based on user weaknesses, and progress tracking that updates mastery scores"

**What Claude generated:**
- Base structure for all three response models
- Field descriptions and type hints
- Literal types for restricted fields (language, difficulty, pattern_type)
- Basic validation rules

**What we modified:**
- Changed pattern_type to include 13 specific error categories relevant to technical interviews (edge_case_missing, suboptimal_time_complexity, etc.)
- Added specific field descriptions matching our capstone requirements
- Wrote our own default values and optional field handling

**Estimate:** ~60% from Claude, 40% our modifications

---

### 2. Function Implementation (Claude + Our Team)

**What Claude helped with:**
- Function signatures with proper type hints
- Docstrings in Google style format
- Try-except error handling pattern
- Basic structure for returning Pydantic models
- UUID generation for submission IDs

**What we wrote ourselves:**
- `MOCK_PROBLEMS` dictionary with three problems (two-sum, reverse-string, valid-parentheses)
- `USER_WEAKNESS_PROFILES` with 13 weakness categories and mastery scores
- `_run_mock_tests()` logic that simulates test execution based on code patterns
- `_detect_error_patterns()` rule-based detection (checks for edge cases, nested loops, data structures)
- `_estimate_complexity()` heuristic for time/space complexity analysis
- Weakness score update algorithm in `track_user_progress()` (decreases by 5 for detected patterns, increases by 3 for clean solutions)
- Problem selection logic in `get_recommended_problem()` that targets weakest area

**Estimate:** ~30% from Claude (structure), 70% our team's logic

---

### 3. Test Suite (Claude + Our Team)

**What we asked:** "Write pytest tests for our three functions that test basic functionality, edge cases (invalid problem ID, nonexistent user), error handling, and performance"

**What Claude generated:**
- Test function templates with proper assertions
- Performance timing test structure using `time.time()`
- Integration test that chains all three functions
- Edge case scenarios (empty code, invalid problem ID, nonexistent user)

**What we customized:**
- Changed expected outputs to match our actual mock data
- Modified test data to use our specific problem IDs ("two-sum", "reverse-string", "valid-parentheses")
- Added tests for specific pattern detection (edge_case_missing, suboptimal_time_complexity)
- Fixed assertions to match our WeaknessScore model structure
- Added test for checking that mastery scores decrease by 5 when patterns detected

**Estimate:** ~65% from Claude, 35% our modifications

---

### 4. Gemini Agent Implementation (Claude)

**What we asked:** "How do we set up Gemini function calling with FunctionDeclaration and handle function_response properly?"

**What Claude helped with:**
- `FunctionDeclaration` structure with proper parameter schemas
- `Tool` object creation with all three functions
- Function calling loop in `send_message()` that handles function_call and function_response
- Error handling with traceback for debugging

**What we wrote:**
- `_execute_function_call()` method that maps function names to our actual functions
- `chat_with_codementor()` convenience function
- Manual function execution for testing (`execute_function()` method)
- Model selection (chose `gemini-2.5-flash` for speed)

**Estimate:** ~50% from Claude (Gemini API boilerplate), 50% our integration logic

---

### 5. GitHub Copilot (Auto-completion)

**Examples from our code:**
- Typed `from pydantic import` → Copilot suggested `BaseModel, Field`
- Typed `class CodeAnalysisResponse(` → Completed with `BaseModel:`
- Typed `MOCK_PROBLEMS = {` → Suggested dictionary structure
- Typing test case dictionaries → Completed `{"input": ..., "expected": ...}` structure

**Helpful:** Saved time on repetitive typing, especially for import statements  
**Not helpful:** Sometimes suggested wrong function names or irrelevant completions

**Estimate:** ~15% of code (small completions)

---

### 6. ChatGPT (Research Only)

**Questions we asked:**
- "What are the most common error patterns in technical interview coding problems?" (used to define our 13 pattern_type categories)
- "How does Gemini function calling differ from OpenAI function calling?" (understanding API differences)
- "Best practices for testing AI-powered functions with mock data?"

**No code generated** - only used for understanding concepts before implementing

---

## What AI Did Well

✅ **Speed:** Cut development time from estimated 6 hours to about 3.5 hours  
✅ **Boilerplate:** Great at generating repetitive code (test cases, model fields, docstrings, import statements)  
✅ **API Integration:** Helped us understand Gemini's FunctionDeclaration format and function_response handling  
✅ **Debugging:** Spotted missing imports and incorrect type hints quickly  
✅ **Documentation:** Generated clear docstrings that we modified to match our specific use cases

---

## What Required Human Work

⚠️ **Project-specific logic:** AI doesn't know CodeMentor AI requirements, so we designed:
- The weakness tracking algorithm (decrease by 5 for detected patterns, increase by 3 for clean code)
- Mock data that matches real technical interview problems
- Pattern detection rules (checking for "if not", "len()", nested loops)
- Integration between all three functions in multi-turn conversations

⚠️ **Mock data realism:** AI generated generic test data, we made it realistic:
- Actual LeetCode-style problems (Two Sum, Valid Parentheses, Reverse String)
- Realistic test case formats (`{"input": "[2,7,11,15], target=9", "expected": "[0,1]"}`)
- User weakness profiles with 13 specific mastery scores

⚠️ **Business rules:** We decided:
- Mastery scores range from 0-100
- Pattern detection triggers 5-point decrease
- Clean solutions trigger 3-point increase across other areas
- Problems target user's weakest area (lowest mastery score)

⚠️ **Error handling:** Added specific error cases AI didn't consider:
- Invalid problem ID returns safe fallback response
- Missing user creates default weakness profile
- Function errors return user-friendly CodeAnalysisResponse with error message

⚠️ **Testing:** Ran all tests multiple times, fixed 3 tests that had incorrect expected values

---

## Learning & Understanding

**How we verified we understand the code:**
1. Read every line of AI-generated code before using it
2. Asked Claude to explain concepts we didn't understand (like Gemini's `content_types.to_content()`)
3. Modified AI code to fit our specific use case
4. Ran all tests to make sure everything works as expected
5. Can explain any part of the code if asked

**Example:** Initially didn't understand how `FunctionDeclaration` parameters work in Gemini. Asked Claude, learned it uses OpenAPI-style JSON schema. Now we confidently use it for all three functions.

**Another example:** Learned about Pydantic's `Literal` type for restricting field values - used it for language ("python", "javascript"), difficulty ("easy", "medium", "hard"), and 13 pattern types.

---

## Notes

- All AI-generated code was reviewed, tested, and understood by our team before submission
- Used AI to accelerate learning and development, not replace understanding
- Total code breakdown: ~40% AI-assisted boilerplate, ~60% human-written business logic
- Every team member can explain and defend the code in our submission
- This log documents AI usage transparently as required by the syllabus
