
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# ========================================
# ENUMS
# ========================================

class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"


class Difficulty(str, Enum):
    """Problem difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    ADAPTIVE = "adaptive"


class ErrorPattern(str, Enum):
    """13 error pattern types we detect"""
    EDGE_CASE_OMISSION = "edge_case_omission"
    SUBOPTIMAL_TIME_COMPLEXITY = "suboptimal_time_complexity"
    SUBOPTIMAL_SPACE_COMPLEXITY = "suboptimal_space_complexity"
    INCORRECT_DATA_STRUCTURE = "incorrect_data_structure"
    OFF_BY_ONE_ERROR = "off_by_one_error"
    BOUNDARY_CONDITION_MISTAKE = "boundary_condition_mistake"
    POOR_VARIABLE_NAMING = "poor_variable_naming"
    MISSING_INPUT_VALIDATION = "missing_input_validation"
    INEFFICIENT_NESTED_LOOPS = "inefficient_nested_loops"
    RECURSION_WITHOUT_BASE_CASE = "recursion_without_base_case"
    IGNORING_CONSTRAINTS = "ignoring_constraints"
    HARDCODING = "hardcoding"
    NOT_HANDLING_DUPLICATES = "not_handling_duplicates"


class ExecutionStatus(str, Enum):
    """Code execution status"""
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    MEMORY_LIMIT = "memory_limit"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"


class Severity(str, Enum):
    """Issue severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ========================================
# CODE EXECUTION MODELS
# ========================================

class TestCase(BaseModel):
    """Single test case for a problem"""
    test_id: int = Field(description="Unique test case identifier")
    input: str = Field(description="Test input as string representation")
    expected_output: str = Field(description="Expected output as string")
    is_hidden: bool = Field(default=False, description="Whether test is hidden from user")


class TestResult(BaseModel):
    """Result of running a single test case"""
    test_id: int
    input: str
    expected_output: str
    actual_output: str
    passed: bool
    execution_time_ms: int = Field(ge=0, description="Execution time in milliseconds")
    error_message: Optional[str] = Field(None, description="Error if test failed")


class CodeExecutionRequest(BaseModel):
    """Request to execute user code"""
    code: str = Field(description="Source code to execute")
    language: Language = Field(description="Programming language")
    problem_id: str = Field(pattern=r"^[a-z0-9-]+$", description="Problem identifier (kebab-case)")
    test_cases: List[TestCase] = Field(min_length=1, description="Test cases to run")
    timeout: int = Field(default=5, ge=1, le=10, description="Max execution time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        if target - num in seen:\n            return [seen[target - num], i]\n        seen[num] = i",
                "language": "python",
                "problem_id": "two-sum",
                "test_cases": [
                    {"test_id": 1, "input": "[2,7,11,15], 9", "expected_output": "[0,1]", "is_hidden": False}
                ],
                "timeout": 5
            }
        }


class CodeExecutionResponse(BaseModel):
    """Response from code execution"""
    status: ExecutionStatus
    execution_time_ms: int = Field(ge=0, description="Total execution time")
    memory_used_kb: int = Field(ge=0, description="Peak memory usage in KB")
    test_results: List[TestResult]
    all_passed: bool
    pass_rate: float = Field(ge=0.0, le=1.0, description="Percentage of tests passed")
    error_type: Optional[str] = Field(None, description="Error type if execution failed")
    error_message: Optional[str] = Field(None, description="Detailed error message")
    line_number: Optional[int] = Field(None, description="Line where error occurred")
    failed_test_case: Optional[TestCase] = Field(None, description="First failed test case")


# ========================================
# CODE ANALYSIS MODELS
# ========================================

class CodeLocation(BaseModel):
    """Location in code where issue occurs"""
    line_start: int = Field(ge=1, description="Starting line number")
    line_end: int = Field(ge=1, description="Ending line number")
    column_start: Optional[int] = Field(None, ge=0, description="Starting column")
    column_end: Optional[int] = Field(None, ge=0, description="Ending column")


class DetectedPattern(BaseModel):
    """Single detected error pattern"""
    pattern_type: ErrorPattern
    confidence: float = Field(ge=0.0, le=1.0, description="ML model confidence score")
    severity: Severity
    description: str = Field(description="Human-readable explanation of the issue")
    code_location: CodeLocation
    suggestion: str = Field(description="Actionable suggestion to fix the issue")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pattern_type": "suboptimal_time_complexity",
                "confidence": 0.92,
                "severity": "high",
                "description": "Using nested loops resulting in O(n²) when O(n) solution exists",
                "code_location": {"line_start": 2, "line_end": 4},
                "suggestion": "Consider using a hash map to achieve O(n) lookup"
            }
        }


class ComplexityAnalysis(BaseModel):
    """Time and space complexity analysis"""
    time_complexity: str = Field(description="Actual time complexity (e.g., 'O(n²)')")
    space_complexity: str = Field(description="Actual space complexity (e.g., 'O(1)')")
    optimal_time: str = Field(description="Known optimal time complexity")
    optimal_space: str = Field(description="Known optimal space complexity")
    is_optimal_time: bool = Field(description="Whether solution achieves optimal time")
    is_optimal_space: bool = Field(description="Whether solution achieves optimal space")


class CodeQualityMetrics(BaseModel):
    """Code quality and readability metrics"""
    cyclomatic_complexity: int = Field(ge=1, description="McCabe complexity score")
    lines_of_code: int = Field(ge=1, description="Total lines of code")
    comment_ratio: float = Field(ge=0.0, le=1.0, description="Ratio of comment lines to code")
    variable_naming_score: float = Field(ge=0.0, le=1.0, description="Variable naming quality")
    readability_score: float = Field(ge=0.0, le=1.0, description="Overall readability")
    function_length_score: float = Field(ge=0.0, le=1.0, description="Function length appropriateness")


class CodeAnalysisRequest(BaseModel):
    """Request to analyze code patterns"""
    user_id: str = Field(pattern=r"^user_[a-z0-9]+$", description="User identifier")
    problem_id: str = Field(pattern=r"^[a-z0-9-]+$", description="Problem identifier")
    code: str = Field(description="Source code to analyze")
    language: Language
    test_results: CodeExecutionResponse = Field(description="Results from code execution")
    optimal_solution: Optional[str] = Field(None, description="Reference optimal solution")


class CodeAnalysisResponse(BaseModel):
    """Response from code analysis"""
    analysis_complete: bool
    detected_patterns: List[DetectedPattern]
    complexity_analysis: ComplexityAnalysis
    code_quality_metrics: CodeQualityMetrics
    weakness_profile_updated: bool
    timestamp: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = Field(None, description="Error if analysis failed")
    message: Optional[str] = Field(None, description="Error details")


# ========================================
# RECOMMENDATION MODELS
# ========================================

class WeaknessSummary(BaseModel):
    """Summary of user's top weaknesses"""
    pattern: ErrorPattern
    mastery_score: int = Field(ge=0, le=100, description="0=weak, 100=mastered")
    occurrences: int = Field(ge=0, description="Number of times this pattern appeared")
    last_seen: datetime = Field(description="When this pattern was last detected")


class ProblemRecommendation(BaseModel):
    """Single recommended problem"""
    problem_id: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str = Field(description="Human-readable problem title")
    difficulty: Literal["easy", "medium", "hard"]
    topics: List[str] = Field(description="Topics covered (e.g., 'arrays', 'hash_maps')")
    estimated_time_minutes: int = Field(ge=5, le=120, description="Expected solve time")
    relevance_score: float = Field(ge=0.0, le=1.0, description="How relevant to user's weaknesses")
    reason: str = Field(description="Why this problem is recommended")
    targeted_weaknesses: List[ErrorPattern] = Field(description="Which weaknesses this addresses")
    success_rate: float = Field(ge=0.0, le=1.0, description="Global success rate for this problem")
    
    class Config:
        json_schema_extra = {
            "example": {
                "problem_id": "contains-duplicate",
                "title": "Contains Duplicate",
                "difficulty": "easy",
                "topics": ["arrays", "hash_maps"],
                "estimated_time_minutes": 15,
                "relevance_score": 0.94,
                "reason": "Targets your weakness: hash map usage for O(n) solutions",
                "targeted_weaknesses": ["suboptimal_time_complexity", "incorrect_data_structure"],
                "success_rate": 0.72
            }
        }


class RecommendationRequest(BaseModel):
    """Request for personalized problem recommendations"""
    user_id: str = Field(pattern=r"^user_[a-z0-9]+$")
    num_recommendations: int = Field(default=3, ge=1, le=10, description="Number of problems to recommend")
    difficulty_preference: Difficulty = Field(default=Difficulty.ADAPTIVE)
    topic_filter: Optional[List[str]] = Field(None, description="Filter by specific topics")
    exclude_recent: bool = Field(default=True, description="Exclude problems attempted recently")


class RecommendationResponse(BaseModel):
    """Response with personalized recommendations"""
    recommendations: List[ProblemRecommendation]
    weakness_summary: Dict[str, Any] = Field(description="Summary of user's weaknesses")
    overall_readiness_score: int = Field(ge=0, le=100, description="Interview readiness score")
    problems_solved: int = Field(ge=0, description="Total problems solved")
    consistency_streak: int = Field(ge=0, description="Days in a row with practice")
    next_milestone: str = Field(description="Next achievement to unlock")


# ========================================
# USER PROFILE MODELS
# ========================================

class UserWeaknessProfile(BaseModel):
    """User's complete weakness profile"""
    user_id: str
    weaknesses: List[WeaknessSummary]
    problems_attempted: int = Field(ge=0)
    problems_solved: int = Field(ge=0)
    average_solve_time_minutes: float = Field(ge=0.0)
    preferred_language: Language
    created_at: datetime
    last_active: datetime


class ProblemAttempt(BaseModel):
    """Record of a single problem attempt"""
    attempt_id: str = Field(description="Unique attempt identifier")
    user_id: str
    problem_id: str
    submitted_at: datetime = Field(default_factory=datetime.now)
    code: str
    language: Language
    execution_result: CodeExecutionResponse
    analysis_result: Optional[CodeAnalysisResponse] = None
    time_spent_seconds: int = Field(ge=0, description="Time spent on problem")
    solved: bool
    attempts_count: int = Field(ge=1, description="Which attempt number this is")


# ========================================
# PROBLEM DATABASE MODELS
# ========================================

class Problem(BaseModel):
    """Complete problem definition"""
    problem_id: str = Field(pattern=r"^[a-z0-9-]+$")
    title: str
    description: str = Field(description="Full problem statement")
    difficulty: Literal["easy", "medium", "hard"]
    topics: List[str]
    test_cases: List[TestCase] = Field(min_length=3, description="At least 3 test cases")
    optimal_time_complexity: str
    optimal_space_complexity: str
    hints: List[str] = Field(default_factory=list, description="Progressive hints")
    related_problems: List[str] = Field(default_factory=list, description="Similar problems")
    target_patterns: List[ErrorPattern] = Field(description="Patterns this problem helps practice")
    
    @field_validator('problem_id')
    @classmethod
    def validate_problem_id(cls, v: str) -> str:
        if not v.islower() or ' ' in v:
            raise ValueError('problem_id must be lowercase kebab-case')
        return v


# ========================================
# ERROR MODELS
# ========================================

class ErrorResponse(BaseModel):
    """Standardized error response"""
    error_code: str = Field(description="Machine-readable error code")
    error_message: str = Field(description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error context")
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = Field(None, description="Request ID for debugging")


# ========================================
# USAGE EXAMPLES
# ========================================

if __name__ == "__main__":
    print("=== CodeMentor AI Pydantic Models - Examples ===\n")
    
    # Example 1: Create a code execution request
    print("Example 1: Code Execution Request")
    exec_request = CodeExecutionRequest(
        code="def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]",
        language=Language.PYTHON,
        problem_id="two-sum",
        test_cases=[
            TestCase(test_id=1, input="[2,7,11,15], 9", expected_output="[0,1]"),
            TestCase(test_id=2, input="[3,2,4], 6", expected_output="[1,2]")
        ],
        timeout=5
    )
    print(exec_request.model_dump_json(indent=2))
    print()
    
    # Example 2: Parse execution response
    print("Example 2: Code Execution Response")
    exec_response = CodeExecutionResponse(
        status=ExecutionStatus.COMPLETED,
        execution_time_ms=124,
        memory_used_kb=2048,
        test_results=[
            TestResult(
                test_id=1,
                input="[2,7,11,15], 9",
                expected_output="[0,1]",
                actual_output="[0,1]",
                passed=True,
                execution_time_ms=12
            )
        ],
        all_passed=True,
        pass_rate=1.0
    )
    print(f"Status: {exec_response.status.value}")
    print(f"All tests passed: {exec_response.all_passed}")
    print(f"Execution time: {exec_response.execution_time_ms}ms")
    print()
    
    # Example 3: Detected pattern with validation
    print("Example 3: Detected Pattern")
    pattern = DetectedPattern(
        pattern_type=ErrorPattern.SUBOPTIMAL_TIME_COMPLEXITY,
        confidence=0.92,
        severity=Severity.HIGH,
        description="Using nested loops resulting in O(n²) when O(n) solution exists",
        code_location=CodeLocation(line_start=2, line_end=4),
        suggestion="Consider using a hash map to achieve O(n) lookup"
    )
    print(pattern.model_dump_json(indent=2))
    print()
    
    # Example 4: Problem recommendation
    print("Example 4: Problem Recommendation")
    recommendation = ProblemRecommendation(
        problem_id="contains-duplicate",
        title="Contains Duplicate",
        difficulty="easy",
        topics=["arrays", "hash_maps"],
        estimated_time_minutes=15,
        relevance_score=0.94,
        reason="Targets your weakness: hash map usage for O(n) solutions",
        targeted_weaknesses=[
            ErrorPattern.SUBOPTIMAL_TIME_COMPLEXITY,
            ErrorPattern.INCORRECT_DATA_STRUCTURE
        ],
        success_rate=0.72
    )
    print(f"Recommended: {recommendation.title}")
    print(f"Relevance: {recommendation.relevance_score:.2f}")
    print(f"Reason: {recommendation.reason}")
    print()
    
    # Example 5: Validation catches errors
    print("Example 5: Validation Error Handling")
    try:
        bad_request = CodeExecutionRequest(
            code="print('hello')",
            language=Language.PYTHON,
            problem_id="Invalid Problem ID!",  # Should fail validation
            test_cases=[],  # Should fail - needs at least 1
            timeout=15  # Should fail - max is 10
        )
    except Exception as e:
        print(f"✓ Validation caught errors:")
        print(f"  {e}")
    print()
    
    # Example 6: Complexity analysis
    print("Example 6: Complexity Analysis")
    complexity = ComplexityAnalysis(
        time_complexity="O(n²)",
        space_complexity="O(1)",
        optimal_time="O(n)",
        optimal_space="O(n)",
        is_optimal_time=False,
        is_optimal_space=True
    )
    print(f"Your solution: {complexity.time_complexity} time, {complexity.space_complexity} space")
    print(f"Optimal: {complexity.optimal_time} time, {complexity.optimal_space} space")
    print(f"Time optimal: {complexity.is_optimal_time}")
    print()
    
    print("=== All examples completed successfully! ===")