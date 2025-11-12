# Evaluation Notes - Week 6 Lab
**Project:** CodeMentor AI  
**Date:** November 11, 2025  
**Team:** AI4ce

---

## Performance Measurements

### Latency Testing

I measured execution time for each function over 5 runs and calculated averages:

| Function | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Average | Status |
|----------|-------|-------|-------|-------|-------|---------|--------|
| `analyze_code_submission()` | 48ms | 42ms | 51ms | 45ms | 44ms | **46ms** | PASS |
| `get_recommended_problem()` | 10ms | 13ms | 11ms | 12ms | 14ms | **12ms** | PASS |
| `track_user_progress()` | 7ms | 9ms | 8ms | 8ms | 8ms | **8ms** | PASS |

**Target:** All functions should complete in < 10 seconds  
**Result:**  All functions complete in < 100ms

---

## Test Cases

### Function 1: `analyze_code_submission()`

| Test Case | Input | Expected Output | Actual Output | Pass/Fail | Time |
|-----------|-------|----------------|---------------|-----------|------|
| Valid code with edge cases | `problem_id="two-sum"`, code with null checks | `all_tests_passed=True`, no edge_case_missing pattern | As expected | PASS | 45ms |
| Code missing edge cases | `problem_id="two-sum"`, code without null checks | `edge_case_missing` pattern detected | Pattern detected | PASS | 42ms |
| Nested loops (O(n²)) | Code with 2 nested for loops | `suboptimal_time_complexity` detected, complexity=O(n²) | Detected correctly | PASS | 51ms |
| Invalid problem ID | `problem_id="fake-problem"` | Error handled gracefully, returns error message | Fallback response | PASS | 38ms |
| Performance test | Standard input | Complete in < 5 seconds | 46ms average | PASS | 46ms |

### Function 2: `get_recommended_problem()`

| Test Case | Input | Expected Output | Actual Output | Pass/Fail | Time |
|-----------|-------|----------------|---------------|-----------|------|
| Easy difficulty | `difficulty="easy"` | Returns easy problem | "two-sum" (easy) | PASS | 12ms |
| Medium difficulty | `difficulty="medium"` | Returns medium problem | "valid-parentheses" | PASS | 13ms |
| Targets weakness | `user_id="user_001"` | Recommendation targets lowest mastery area | Targets edge_case_missing (45/100) | PASS | 11ms |
| Invalid user ID | `user_id="fake_user"` | Fallback recommendation | Returns default problem | PASS | 10ms |

### Function 3: `track_user_progress()`

| Test Case | Input | Expected Output | Actual Output | Pass/Fail | Time |
|-----------|-------|----------------|---------------|-----------|------|
| Detected pattern updates | `detected_patterns=["edge_case_missing"]` | Mastery score decreases for that pattern | Score: 45→40 | PASS | 8ms |
| Solved correctly | `solved_correctly=True`, no patterns | Scores improve for non-detected patterns | Multiple improving trends | PASS | 9ms |
| Multiple patterns | 3 patterns detected | All 3 pattern scores updated | All updated correctly | PASS | 8ms |
| Next focus identified | Any valid input | Returns weakest area | Returns "edge_case_missing" | PASS | 7ms |

---

## Error Handling Tests

| Scenario | Expected Behavior | Actual Behavior | Status |
|----------|------------------|-----------------|--------|
| Missing API key | Graceful error message | Returns error without crash | PASS |
| Invalid problem ID | Fallback response | Returns safe response | PASS |
| Malformed user code | Parse safely | Handles without crash | PASS |
| Empty input strings | Validation error or safe default | Pydantic validates, returns defaults | PASS |
| Nonexistent user ID | Create fallback profile | Returns default weakness profile | PASS |

---

## Integration Test Results

**Full Workflow Test:** Analyze → Track → Recommend

```
1. analyze_code_submission() → Detected patterns: ["edge_case_missing"]
2. track_user_progress() → Updated scores, overall_mastery: 58.3
3. get_recommended_problem() → Recommended "valid-parentheses" (targets edge cases)
```

**Result:** PASS - All functions work together correctly

---

## Summary

- All 16 unit tests passing
- All functions complete in < 100ms (well under 10s target)
- Error handling works for all edge cases
- Integration test passes end-to-end
- Pydantic validation prevents invalid inputs

