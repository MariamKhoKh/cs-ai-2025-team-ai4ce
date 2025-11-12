import time
import uuid
from datetime import datetime
from typing import List
from src.backend.models.function_models import (
    CodeSubmissionRequest, CodeAnalysisResponse, TestResult, ErrorPattern,
    ProblemRecommendationRequest, RecommendationResponse, Problem,
    ProgressTrackingRequest, ProgressTrackingResponse, WeaknessScore
)


# ==================== Mock Data ====================

MOCK_PROBLEMS = {
    "two-sum": {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of two numbers that add up to target.",
        "difficulty": "easy",
        "test_cases": [
            {"input": "[2,7,11,15], target=9", "expected": "[0,1]"},
            {"input": "[3,2,4], target=6", "expected": "[1,2]"},
            {"input": "[3,3], target=6", "expected": "[0,1]"}
        ]
    },
    "reverse-string": {
        "title": "Reverse String",
        "description": "Write a function that reverses a string. The input string is given as an array of characters.",
        "difficulty": "easy",
        "test_cases": [
            {"input": "['h','e','l','l','o']", "expected": "['o','l','l','e','h']"},
            {"input": "['H','a','n','n','a','h']", "expected": "['h','a','n','n','a','H']"}
        ]
    },
    "valid-parentheses": {
        "title": "Valid Parentheses",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "difficulty": "medium",
        "test_cases": [
            {"input": "'()'", "expected": "true"},
            {"input": "'()[]{}'", "expected": "true"},
            {"input": "'(]'", "expected": "false"}
        ]
    }
}

# Mock user weakness profiles (in real app, this would be in database)
USER_WEAKNESS_PROFILES = {
    "user_001": {
        "edge_case_missing": 45.0,
        "suboptimal_time_complexity": 60.0,
        "wrong_data_structure": 50.0,
        "off_by_one": 70.0,
        "boundary_condition": 55.0,
        "poor_naming": 80.0,
        "missing_validation": 40.0,
        "inefficient_loops": 65.0,
        "missing_base_case": 75.0,
        "ignoring_constraints": 50.0,
        "hardcoding": 85.0,
        "duplicate_handling": 55.0,
        "suboptimal_space_complexity": 60.0
    }
}


# ==================== Function 1: Code Analysis ====================

def analyze_code_submission(
    problem_id: str,
    user_code: str,
    language: str = "python",
    user_id: str = "user_001"
) -> CodeAnalysisResponse:
    """
    Analyze user's code submission and detect error patterns.
    
    Args:
        problem_id: Problem identifier
        user_code: User's submitted code
        language: Programming language (python/javascript)
        user_id: User identifier
    
    Returns:
        CodeAnalysisResponse with test results, detected patterns, and AI feedback
    """
    start_time = time.time()
    
    try:
        # Generate unique submission ID
        submission_id = f"sub_{uuid.uuid4().hex[:8]}"
        
        # Mock test execution (in real app, would use Judge0/Piston)
        test_results = _run_mock_tests(problem_id, user_code)
        all_passed = all(test.passed for test in test_results)
        
        # Detect error patterns (mock analysis)
        detected_patterns = _detect_error_patterns(user_code, all_passed)
        
        # Generate AI feedback (mock for now, will use Gemini later)
        ai_feedback = _generate_mock_feedback(problem_id, detected_patterns, all_passed)
        
        # Estimate complexity (simple heuristic)
        time_complexity, space_complexity = _estimate_complexity(user_code)
        
        execution_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return CodeAnalysisResponse(
            submission_id=submission_id,
            problem_id=problem_id,
            test_results=test_results,
            all_tests_passed=all_passed,
            detected_patterns=detected_patterns,
            ai_feedback=ai_feedback,
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            execution_time_ms=round(execution_time, 2),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        # Error handling: return safe response
        return CodeAnalysisResponse(
            submission_id=f"sub_error_{uuid.uuid4().hex[:8]}",
            problem_id=problem_id,
            test_results=[],
            all_tests_passed=False,
            detected_patterns=[],
            ai_feedback=f"Error analyzing code: {str(e)}",
            time_complexity="Unknown",
            space_complexity="Unknown",
            execution_time_ms=0.0,
            timestamp=datetime.now().isoformat()
        )


def _run_mock_tests(problem_id: str, user_code: str) -> List[TestResult]:
    """Mock test execution (replace with real sandbox later)"""
    if problem_id not in MOCK_PROBLEMS:
        return [TestResult(
            test_name="Unknown Problem",
            passed=False,
            expected="N/A",
            actual="N/A",
            error_message="Problem not found"
        )]
    
    # Simulate test results based on code quality indicators
    has_edge_case_handling = "if not" in user_code or "len(" in user_code
    
    test_cases = MOCK_PROBLEMS[problem_id]["test_cases"]
    results = []
    
    for i, test_case in enumerate(test_cases):
        # Simple heuristic: pass basic tests, fail edge cases if no handling
        passed = i < 2 or has_edge_case_handling
        
        results.append(TestResult(
            test_name=f"Test {i+1}",
            passed=passed,
            expected=test_case["expected"],
            actual=test_case["expected"] if passed else "Wrong Answer",
            error_message=None if passed else "Edge case not handled"
        ))
    
    return results


def _detect_error_patterns(user_code: str, all_passed: bool) -> List[ErrorPattern]:
    """Detect error patterns in code (simplified rule-based for now)"""
    patterns = []
    
    # Check for edge case handling
    if "if not" not in user_code and "len(" not in user_code:
        patterns.append(ErrorPattern(
            pattern_type="edge_case_missing",
            severity="high",
            description="Code doesn't check for empty or null inputs"
        ))
    
    # Check for nested loops (complexity issue)
    if user_code.count("for") >= 2 and "for" in user_code:
        patterns.append(ErrorPattern(
            pattern_type="suboptimal_time_complexity",
            severity="medium",
            description="Nested loops detected - may have O(n²) complexity"
        ))
    
    # Check for list usage where dict might be better
    if "in range" in user_code and "[" in user_code and "{" not in user_code:
        patterns.append(ErrorPattern(
            pattern_type="wrong_data_structure",
            severity="low",
            description="Using list when hash map might be more efficient"
        ))
    
    return patterns


def _generate_mock_feedback(problem_id: str, patterns: List[ErrorPattern], all_passed: bool) -> str:
    """Generate mock AI feedback (will use Gemini in Part 4)"""
    if all_passed and not patterns:
        return "Great job! Your solution passes all tests and shows good coding practices."
    
    feedback = "Here's what I noticed:\n\n"
    
    if not all_passed:
        feedback += "Some test cases failed. Focus on edge cases like empty inputs.\n\n"
    
    if patterns:
        feedback += "Detected patterns:\n"
        for p in patterns:
            feedback += f"- {p.pattern_type}: {p.description}\n"
    
    feedback += "\nNext steps: Try to handle edge cases first, then optimize complexity."
    
    return feedback


def _estimate_complexity(code: str) -> tuple[str, str]:
    """Simple heuristic for complexity estimation"""
    nested_loops = code.count("for") + code.count("while")
    
    if nested_loops >= 2:
        time = "O(n²)"
    elif nested_loops == 1:
        time = "O(n)"
    else:
        time = "O(1)"
    
    # Check for extra data structures
    has_extra_storage = "{" in code or "[]" in code
    space = "O(n)" if has_extra_storage else "O(1)"
    
    return time, space


# ==================== Function 2: Problem Recommendation ====================

def get_recommended_problem(
    user_id: str = "user_001",
    difficulty_level: str = "easy"
) -> RecommendationResponse:
    """
    Recommend next problem based on user's weakness profile.
    
    Args:
        user_id: User identifier
        difficulty_level: Desired difficulty (easy/medium/hard)
    
    Returns:
        RecommendationResponse with problem details and reasoning
    """
    try:
        # Get user's weakness profile
        weaknesses = USER_WEAKNESS_PROFILES.get(user_id, {})
        
        # Find top 3 weakest areas (lowest scores)
        sorted_weaknesses = sorted(weaknesses.items(), key=lambda x: x[1])
        top_weaknesses = [w[0] for w in sorted_weaknesses[:3]]
        
        # Select problem that targets weakest area
        target_pattern = top_weaknesses[0] if top_weaknesses else "edge_case_missing"
        
        # Pick a problem based on difficulty
        if difficulty_level == "easy":
            problem_id = "two-sum"
        elif difficulty_level == "medium":
            problem_id = "valid-parentheses"
        else:
            problem_id = "reverse-string"
        
        problem_data = MOCK_PROBLEMS[problem_id]
        
        recommended_problem = Problem(
            problem_id=problem_id,
            title=problem_data["title"],
            description=problem_data["description"],
            difficulty=problem_data["difficulty"],
            target_patterns=[target_pattern],
            estimated_time_minutes=15 if difficulty_level == "easy" else 30
        )
        
        reason = f"This problem targets your weakest area: {target_pattern.replace('_', ' ')}. "
        reason += f"Your current mastery: {weaknesses.get(target_pattern, 50):.0f}/100"
        
        return RecommendationResponse(
            recommended_problem=recommended_problem,
            recommendation_reason=reason,
            user_weakness_areas=top_weaknesses
        )
    
    except Exception as e:
        # Fallback recommendation
        return RecommendationResponse(
            recommended_problem=Problem(
                problem_id="two-sum",
                title="Two Sum",
                description="Fallback problem",
                difficulty="easy",
                target_patterns=["general_practice"],
                estimated_time_minutes=15
            ),
            recommendation_reason=f"Error loading recommendation: {str(e)}",
            user_weakness_areas=["general_practice"]
        )


# ==================== Function 3: Progress Tracking ====================

def track_user_progress(
    user_id: str,
    problem_id: str,
    detected_patterns: List[str],
    time_taken_minutes: float,
    attempts_count: int,
    solved_correctly: bool
) -> ProgressTrackingResponse:
    """
    Update user's weakness profile after problem submission.
    
    Args:
        user_id: User identifier
        problem_id: Problem that was attempted
        detected_patterns: Error patterns found in submission
        time_taken_minutes: Time spent on problem
        attempts_count: Number of attempts made
        solved_correctly: Whether problem was solved
    
    Returns:
        ProgressTrackingResponse with updated weakness scores
    """
    try:
        # Get current profile
        profile = USER_WEAKNESS_PROFILES.get(user_id, {}).copy()
        
        # Update scores based on detected patterns
        updated_weaknesses = []
        
        for pattern_type in profile.keys():
            current_score = profile[pattern_type]
            
            if pattern_type in detected_patterns:
                # Pattern detected = weakness confirmed, decrease score slightly
                new_score = max(0, current_score - 5)
                trend = "declining"
            elif solved_correctly:
                # Solved without this pattern = improvement
                new_score = min(100, current_score + 3)
                trend = "improving"
            else:
                new_score = current_score
                trend = "stable"
            
            updated_weaknesses.append(WeaknessScore(
                pattern_type=pattern_type,
                mastery_score=round(new_score, 1),
                trend=trend,
                problems_attempted=10  # Mock value
            ))
            
            # Update profile in memory
            profile[pattern_type] = new_score
        
        # Calculate overall mastery
        overall = sum(profile.values()) / len(profile)
        
        # Find weakest area for next focus
        weakest = min(profile.items(), key=lambda x: x[1])
        next_focus = weakest[0]
        
        return ProgressTrackingResponse(
            user_id=user_id,
            updated_weaknesses=updated_weaknesses,
            overall_mastery=round(overall, 1),
            next_focus_area=next_focus,
            problems_solved_total=25,  # Mock value
            streak_days=3,  # Mock value
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        # Return safe fallback
        return ProgressTrackingResponse(
            user_id=user_id,
            updated_weaknesses=[],
            overall_mastery=50.0,
            next_focus_area="general_practice",
            problems_solved_total=0,
            streak_days=0,
            timestamp=datetime.now().isoformat()
        )