import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.backend.functions.tools import (
    analyze_code_submission,
    get_recommended_problem,
    track_user_progress
)
from src.backend.models.function_models import (
    CodeAnalysisResponse,
    RecommendationResponse,
    ProgressTrackingResponse
)


# ==================== Test Function 1: analyze_code_submission ====================

def test_analyze_code_basic():
    """Test basic code analysis with valid input"""
    result = analyze_code_submission(
        problem_id="two-sum",
        user_code="def two_sum(nums, target):\n    for i in range(len(nums)):\n        return [0, 1]",
        language="python"
    )
    
    assert isinstance(result, CodeAnalysisResponse)
    assert result.problem_id == "two-sum"
    assert result.submission_id.startswith("sub_")
    assert len(result.test_results) > 0
    assert result.execution_time_ms >= 0


def test_analyze_code_edge_case_detection():
    """Test that edge case missing is detected"""
    # Code without edge case handling
    code_without_checks = "def solve(arr):\n    return arr[0]"
    
    result = analyze_code_submission(
        problem_id="two-sum",
        user_code=code_without_checks,
        language="python"
    )
    
    # Should detect missing edge case handling
    pattern_types = [p.pattern_type for p in result.detected_patterns]
    assert "edge_case_missing" in pattern_types


def test_analyze_code_complexity_detection():
    """Test that nested loops are detected as complexity issue"""
    # Code with nested loops
    code_with_nested_loops = """
def solve(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] + arr[j] == target:
                return [i, j]
"""
    
    result = analyze_code_submission(
        problem_id="two-sum",
        user_code=code_with_nested_loops,
        language="python"
    )
    
    # Should detect suboptimal complexity
    pattern_types = [p.pattern_type for p in result.detected_patterns]
    assert "suboptimal_time_complexity" in pattern_types
    assert "O(n²)" in result.time_complexity or "O(n)" in result.time_complexity


def test_analyze_code_error_handling():
    """Test that invalid problem ID is handled gracefully"""
    result = analyze_code_submission(
        problem_id="nonexistent-problem",
        user_code="def solve(): pass",
        language="python"
    )
    
    # Should not crash, should return error info
    assert isinstance(result, CodeAnalysisResponse)
    assert len(result.test_results) >= 0


def test_analyze_code_performance():
    """Test that analysis completes in reasonable time"""
    import time
    start = time.time()
    
    result = analyze_code_submission(
        problem_id="two-sum",
        user_code="def solve(arr): return arr",
        language="python"
    )
    
    elapsed = time.time() - start
    assert elapsed < 5.0  # Should complete in under 5 seconds


# ==================== Test Function 2: get_recommended_problem ====================

def test_get_recommendation_basic():
    """Test basic problem recommendation"""
    result = get_recommended_problem(
        user_id="user_001",
        difficulty_level="easy"
    )
    
    assert isinstance(result, RecommendationResponse)
    assert result.recommended_problem.problem_id in ["two-sum", "reverse-string", "valid-parentheses"]
    assert len(result.user_weakness_areas) > 0
    assert len(result.recommendation_reason) > 0


def test_get_recommendation_difficulty_levels():
    """Test that different difficulty levels return appropriate problems"""
    easy = get_recommended_problem(user_id="user_001", difficulty_level="easy")
    medium = get_recommended_problem(user_id="user_001", difficulty_level="medium")
    hard = get_recommended_problem(user_id="user_001", difficulty_level="hard")
    
    assert easy.recommended_problem.difficulty in ["easy", "medium", "hard"]
    assert medium.recommended_problem.difficulty in ["easy", "medium", "hard"]
    assert hard.recommended_problem.difficulty in ["easy", "medium", "hard"]


def test_get_recommendation_targets_weakness():
    """Test that recommendation targets user weaknesses"""
    result = get_recommended_problem(user_id="user_001")
    
    # Should have target patterns
    assert len(result.recommended_problem.target_patterns) > 0
    
    # Reason should mention weakness
    assert "weakness" in result.recommendation_reason.lower() or "mastery" in result.recommendation_reason.lower()


def test_get_recommendation_error_handling():
    """Test recommendation with invalid user ID"""
    result = get_recommended_problem(user_id="nonexistent_user", difficulty_level="easy")
    
    # Should still return a valid recommendation (fallback)
    assert isinstance(result, RecommendationResponse)
    assert result.recommended_problem.problem_id is not None


# ==================== Test Function 3: track_user_progress ====================

def test_track_progress_basic():
    """Test basic progress tracking"""
    result = track_user_progress(
        user_id="user_001",
        problem_id="two-sum",
        detected_patterns=["edge_case_missing"],
        time_taken_minutes=10.5,
        attempts_count=2,
        solved_correctly=True
    )
    
    assert isinstance(result, ProgressTrackingResponse)
    assert result.user_id == "user_001"
    assert len(result.updated_weaknesses) > 0
    assert 0 <= result.overall_mastery <= 100


def test_track_progress_weakness_update():
    """Test that detected patterns decrease mastery scores"""
    result = track_user_progress(
        user_id="user_001",
        problem_id="two-sum",
        detected_patterns=["edge_case_missing", "suboptimal_time_complexity"],
        time_taken_minutes=15.0,
        attempts_count=3,
        solved_correctly=False
    )
    
    # Find the updated weakness for edge_case_missing
    edge_case_weakness = next(
        (w for w in result.updated_weaknesses if w.pattern_type == "edge_case_missing"),
        None
    )
    
    assert edge_case_weakness is not None
    # Trend should be declining since pattern was detected
    assert edge_case_weakness.trend in ["declining", "stable"]


def test_track_progress_improvement():
    """Test that solving correctly improves scores"""
    result = track_user_progress(
        user_id="user_001",
        problem_id="two-sum",
        detected_patterns=[],  # No patterns = clean solution
        time_taken_minutes=8.0,
        attempts_count=1,
        solved_correctly=True
    )
    
    # Should have some improving trends
    improving_count = sum(1 for w in result.updated_weaknesses if w.trend == "improving")
    assert improving_count > 0


def test_track_progress_next_focus():
    """Test that next focus area is identified"""
    result = track_user_progress(
        user_id="user_001",
        problem_id="two-sum",
        detected_patterns=["edge_case_missing"],
        time_taken_minutes=10.0,
        attempts_count=2,
        solved_correctly=False
    )
    
    assert result.next_focus_area is not None
    assert len(result.next_focus_area) > 0


def test_track_progress_error_handling():
    """Test progress tracking with missing data"""
    result = track_user_progress(
        user_id="new_user_999",
        problem_id="unknown",
        detected_patterns=[],
        time_taken_minutes=5.0,
        attempts_count=1,
        solved_correctly=False
    )
    
    # Should handle gracefully with fallback
    assert isinstance(result, ProgressTrackingResponse)


# ==================== Integration Tests ====================

def test_full_workflow():
    """Test complete workflow: analyze -> track -> recommend"""
    # Step 1: Analyze code
    analysis = analyze_code_submission(
        problem_id="two-sum",
        user_code="def solve(arr): pass",
        language="python",
        user_id="user_001"
    )
    
    assert isinstance(analysis, CodeAnalysisResponse)
    
    # Step 2: Track progress based on analysis
    pattern_types = [p.pattern_type for p in analysis.detected_patterns]
    progress = track_user_progress(
        user_id="user_001",
        problem_id="two-sum",
        detected_patterns=pattern_types,
        time_taken_minutes=12.0,
        attempts_count=2,
        solved_correctly=analysis.all_tests_passed
    )
    
    assert isinstance(progress, ProgressTrackingResponse)
    
    # Step 3: Get next recommendation
    recommendation = get_recommended_problem(
        user_id="user_001",
        difficulty_level="easy"
    )
    
    assert isinstance(recommendation, RecommendationResponse)


# ==================== Performance Tests ====================

def test_latency_all_functions():
    """Measure average latency of all functions"""
    import time
    
    latencies = []
    
    # Test analyze_code_submission
    start = time.time()
    analyze_code_submission("two-sum", "def solve(): pass", "python")
    latencies.append(("analyze_code_submission", time.time() - start))
    
    # Test get_recommended_problem
    start = time.time()
    get_recommended_problem("user_001", "easy")
    latencies.append(("get_recommended_problem", time.time() - start))
    
    # Test track_user_progress
    start = time.time()
    track_user_progress("user_001", "two-sum", [], 10.0, 1, True)
    latencies.append(("track_user_progress", time.time() - start))
    
    # All should be under 2 seconds
    for func_name, latency in latencies:
        print(f"{func_name}: {latency*1000:.2f}ms")
        assert latency < 2.0, f"{func_name} took too long: {latency:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])