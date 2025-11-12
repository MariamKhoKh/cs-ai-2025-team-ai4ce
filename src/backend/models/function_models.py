from pydantic import BaseModel, Field
from typing import List, Literal, Dict
from datetime import datetime


# ==================== Function 1: analyze_code_submission ====================

class CodeSubmissionRequest(BaseModel):
    """Input model for code analysis"""
    problem_id: str = Field(description="Problem ID (e.g., 'two-sum', 'reverse-string')")
    user_code: str = Field(description="User's submitted code as a string")
    language: Literal["python", "javascript"] = Field(description="Programming language")
    user_id: str = Field(default="user_001", description="User identifier")


class TestResult(BaseModel):
    """Individual test case result"""
    test_name: str
    passed: bool
    expected: str
    actual: str
    error_message: str | None = None


class ErrorPattern(BaseModel):
    """Detected error pattern in user's code"""
    pattern_type: Literal[
        "edge_case_missing",
        "suboptimal_time_complexity",
        "suboptimal_space_complexity",
        "wrong_data_structure",
        "off_by_one",
        "boundary_condition",
        "poor_naming",
        "missing_validation",
        "inefficient_loops",
        "missing_base_case",
        "ignoring_constraints",
        "hardcoding",
        "duplicate_handling"
    ]
    severity: Literal["low", "medium", "high"]
    description: str


class CodeAnalysisResponse(BaseModel):
    """Output model for code analysis"""
    submission_id: str
    problem_id: str
    test_results: List[TestResult]
    all_tests_passed: bool
    detected_patterns: List[ErrorPattern]
    ai_feedback: str = Field(description="GPT/Gemini explanation of mistakes")
    time_complexity: str = Field(description="Estimated time complexity (e.g., O(n))")
    space_complexity: str = Field(description="Estimated space complexity")
    execution_time_ms: float
    timestamp: str


# ==================== Function 2: get_recommended_problem ====================

class ProblemRecommendationRequest(BaseModel):
    """Input model for problem recommendation"""
    user_id: str = Field(default="user_001", description="User identifier")
    difficulty_level: Literal["easy", "medium", "hard"] = Field(
        default="easy",
        description="Current difficulty preference"
    )


class Problem(BaseModel):
    """Problem details"""
    problem_id: str
    title: str
    description: str
    difficulty: Literal["easy", "medium", "hard"]
    target_patterns: List[str] = Field(description="Error patterns this problem targets")
    estimated_time_minutes: int


class RecommendationResponse(BaseModel):
    """Output model for problem recommendation"""
    recommended_problem: Problem
    recommendation_reason: str = Field(
        description="Why this problem was recommended (which weakness it targets)"
    )
    user_weakness_areas: List[str] = Field(
        description="User's current top 3 weakness areas"
    )


# ==================== Function 3: track_user_progress ====================

class ProgressTrackingRequest(BaseModel):
    """Input model for progress tracking"""
    user_id: str = Field(default="user_001", description="User identifier")
    problem_id: str
    detected_patterns: List[str] = Field(description="Error pattern types detected")
    time_taken_minutes: float
    attempts_count: int
    solved_correctly: bool


class WeaknessScore(BaseModel):
    """Score for a specific weakness category"""
    pattern_type: str
    mastery_score: float = Field(ge=0, le=100, description="0-100, higher is better")
    trend: Literal["improving", "stable", "declining"]
    problems_attempted: int


class ProgressTrackingResponse(BaseModel):
    """Output model for progress tracking"""
    user_id: str
    updated_weaknesses: List[WeaknessScore]
    overall_mastery: float = Field(ge=0, le=100, description="Average mastery across all patterns")
    next_focus_area: str = Field(description="Which pattern to focus on next")
    problems_solved_total: int
    streak_days: int
    timestamp: str