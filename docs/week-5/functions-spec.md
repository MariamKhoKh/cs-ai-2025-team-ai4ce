Function Calling Specification - CodeMentor AI
Project: CodeMentor AI - Technical Interview Prep with Personalized Weakness Detection
Team: AI4ce
Date: November 6, 2025

Overview
This document specifies the core functions that the AI assistant in CodeMentor will call to analyze code, provide feedback, and personalize the learning experience. These functions enable the AI to take actions beyond conversation—executing code, analyzing patterns, and adapting to user weaknesses.

Core Functions
Function 1: execute_code
Purpose: Execute user-submitted code in a sandboxed environment and return test results

When AI should call this:

User submits code solution for a problem
User clicks "Run Code" or "Submit Solution"
AI needs to verify if code passes test cases before providing feedback
Parameters:

code (string, required): The source code submitted by the user
language (string, required): Programming language ("python" or "javascript")
problem_id (string, required): Unique identifier for the problem being solved
test_cases (array, required): Array of test case objects with inputs and expected outputs
timeout (integer, optional): Maximum execution time in seconds, default: 5
Returns:

Success:

json
{
  "status": "completed",
  "execution_time_ms": 124,
  "memory_used_kb": 2048,
  "test_results": [
    {
      "test_id": 1,
      "input": "[2,7,11,15], target=9",
      "expected_output": "[0,1]",
      "actual_output": "[0,1]",
      "passed": true,
      "execution_time_ms": 12
    },
    {
      "test_id": 2,
      "input": "[3,2,4], target=6",
      "expected_output": "[1,2]",
      "actual_output": "[1,2]",
      "passed": true,
      "execution_time_ms": 8
    }
  ],
  "all_passed": true,
  "pass_rate": 1.0
}
Error:

json
{
  "status": "error",
  "error_type": "runtime_error",
  "error_message": "IndexError: list index out of range",
  "line_number": 5,
  "failed_test_case": {
    "test_id": 3,
    "input": "[], target=0"
  }
}
JSON Schema:

json
{
  "name": "execute_code",
  "description": "Execute user code in a sandboxed environment (Judge0/Piston) and return test results. Returns execution time, memory usage, and pass/fail status for each test case.",
  "parameters": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "description": "The complete source code to execute"
      },
      "language": {
        "type": "string",
        "enum": ["python", "javascript"],
        "description": "Programming language of the submitted code"
      },
      "problem_id": {
        "type": "string",
        "description": "Unique identifier for the problem (e.g., 'two-sum', 'valid-parentheses')"
      },
      "test_cases": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "test_id": {"type": "integer"},
            "input": {"type": "string"},
            "expected_output": {"type": "string"}
          }
        },
        "description": "Array of test cases to run against the code"
      },
      "timeout": {
        "type": "integer",
        "description": "Maximum execution time in seconds",
        "default": 5,
        "minimum": 1,
        "maximum": 10
      }
    },
    "required": ["code", "language", "problem_id", "test_cases"]
  }
}
Example Call:

python
result = execute_code(
    code='def twoSum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i+1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]',
    language="python",
    problem_id="two-sum",
    test_cases=[
        {"test_id": 1, "input": "[2,7,11,15], 9", "expected_output": "[0,1]"},
        {"test_id": 2, "input": "[3,2,4], 6", "expected_output": "[1,2]"}
    ]
)
# Returns: {"status": "completed", "all_passed": true, "execution_time_ms": 124, ...}
Safety Considerations:

Code executed in isolated sandbox (Judge0/Piston API) - NEVER on our servers
Strict timeout limits (max 10 seconds) to prevent infinite loops
Memory limits enforced (max 256MB per execution)
Rate limit: 20 executions per user per hour
Input sanitization to prevent code injection
Log all executions for security auditing
Function 2: analyze_code_patterns
Purpose: Analyze submitted code using AST parsing and ML classification to detect error patterns and weaknesses

When AI should call this:

After code execution completes (whether passed or failed)
User requests detailed feedback on their solution
AI needs to identify specific weaknesses to explain or recommend next problem
Parameters:

user_id (string, required): Unique identifier for the user
problem_id (string, required): Problem being analyzed
code (string, required): The source code to analyze
language (string, required): Programming language
test_results (object, required): Results from execute_code function
optimal_solution (string, optional): Reference optimal solution for comparison
Returns:

Success:

json
{
  "analysis_complete": true,
  "detected_patterns": [
    {
      "pattern_type": "suboptimal_time_complexity",
      "confidence": 0.92,
      "severity": "high",
      "description": "Using nested loops resulting in O(n²) when O(n) solution exists",
      "code_location": {"line_start": 2, "line_end": 4},
      "suggestion": "Consider using a hash map to achieve O(n) lookup"
    },
    {
      "pattern_type": "missing_edge_case",
      "confidence": 0.78,
      "severity": "medium",
      "description": "Code does not handle empty array input",
      "code_location": {"line_start": 1, "line_end": 1},
      "suggestion": "Add validation: if not nums: return []"
    }
  ],
  "complexity_analysis": {
    "time_complexity": "O(n²)",
    "space_complexity": "O(1)",
    "optimal_time": "O(n)",
    "optimal_space": "O(n)"
  },
  "code_quality_metrics": {
    "cyclomatic_complexity": 3,
    "lines_of_code": 12,
    "variable_naming_score": 0.85,
    "readability_score": 0.78
  },
  "weakness_profile_updated": true
}
Error:

json
{
  "analysis_complete": false,
  "error": "ast_parse_failure",
  "message": "Syntax error in submitted code prevents analysis"
}
JSON Schema:

json
{
  "name": "analyze_code_patterns",
  "description": "Analyze code structure using AST parsing and ML classification to detect error patterns, complexity issues, and coding weaknesses. Updates user's weakness profile for personalized recommendations.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "Unique user identifier for profile tracking"
      },
      "problem_id": {
        "type": "string",
        "description": "Problem identifier for context"
      },
      "code": {
        "type": "string",
        "description": "Source code to analyze"
      },
      "language": {
        "type": "string",
        "enum": ["python", "javascript"],
        "description": "Programming language"
      },
      "test_results": {
        "type": "object",
        "description": "Test execution results from execute_code function"
      },
      "optimal_solution": {
        "type": "string",
        "description": "Reference optimal solution for comparison (optional)"
      }
    },
    "required": ["user_id", "problem_id", "code", "language", "test_results"]
  }
}
Example Call:

python
analysis = analyze_code_patterns(
    user_id="user_abc123",
    problem_id="two-sum",
    code='def twoSum(nums, target): ...',
    language="python",
    test_results={"all_passed": true, "execution_time_ms": 124}
)
# Returns: {
#   "detected_patterns": [
#     {"pattern_type": "suboptimal_time_complexity", "confidence": 0.92, ...}
#   ],
#   "complexity_analysis": {"time_complexity": "O(n²)", "optimal_time": "O(n)"}
# }
Safety Considerations:

AST parsing isolated from execution environment
ML model predictions include confidence scores - flag low-confidence results
Store analysis history for model retraining
Rate limit: 30 analyses per user per hour
Validate user_id ownership before updating profile
Handle parse failures gracefully (syntax errors)
Privacy: Anonymize code samples used for model training
Function 3: get_personalized_recommendation
Purpose: Recommend the next problem based on user's weakness profile and learning progression

When AI should call this:

User completes a problem and asks "What should I practice next?"
User opens dashboard and requests recommendations
User clicks "Get Next Problem" button
AI suggests practice path after analyzing performance
Parameters:

user_id (string, required): Unique identifier for the user
num_recommendations (integer, optional): Number of problems to recommend, default: 3
difficulty_preference (string, optional): User's preferred difficulty level ("easy", "medium", "hard", "adaptive")
topic_filter (array, optional): Specific topics to focus on (e.g., ["arrays", "hash_maps"])
exclude_recent (boolean, optional): Exclude recently attempted problems, default: true
Returns:

Success:

json
{
  "recommendations": [
    {
      "problem_id": "contains-duplicate",
      "title": "Contains Duplicate",
      "difficulty": "easy",
      "topics": ["arrays", "hash_maps"],
      "estimated_time_minutes": 15,
      "relevance_score": 0.94,
      "reason": "Targets your weakness: hash map usage for O(n) solutions. Similar structure to previous attempts.",
      "targeted_weaknesses": ["suboptimal_time_complexity", "data_structure_choice"],
      "success_rate": 0.72
    },
    {
      "problem_id": "valid-anagram",
      "title": "Valid Anagram",
      "difficulty": "easy",
      "topics": ["strings", "hash_maps"],
      "estimated_time_minutes": 12,
      "relevance_score": 0.88,
      "reason": "Strengthens hash map pattern recognition and edge case handling",
      "targeted_weaknesses": ["missing_edge_case", "data_structure_choice"],
      "success_rate": 0.81
    }
  ],
  "weakness_summary": {
    "top_weaknesses": [
      {"pattern": "suboptimal_time_complexity", "mastery_score": 32},
      {"pattern": "missing_edge_case", "mastery_score": 45},
      {"pattern": "data_structure_choice", "mastery_score": 51}
    ],
    "overall_readiness_score": 58,
    "problems_solved": 12,
    "consistency_streak": 5
  }
}
JSON Schema:

json
{
  "name": "get_personalized_recommendation",
  "description": "Generate personalized problem recommendations based on user's weakness profile, learning progression, and mastery scores. Uses collaborative filtering and adaptive difficulty adjustment.",
  "parameters": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "Unique user identifier"
      },
      "num_recommendations": {
        "type": "integer",
        "description": "Number of problems to recommend",
        "default": 3,
        "minimum": 1,
        "maximum": 10
      },
      "difficulty_preference": {
        "type": "string",
        "enum": ["easy", "medium", "hard", "adaptive"],
        "description": "Preferred difficulty level. 'adaptive' adjusts based on recent performance.",
        "default": "adaptive"
      },
      "topic_filter": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["arrays", "strings", "hash_maps", "trees", "graphs", "dynamic_programming"]
        },
        "description": "Filter recommendations to specific topics"
      },
      "exclude_recent": {
        "type": "boolean",
        "description": "Exclude problems attempted in last 7 days",
        "default": true
      }
    },
    "required": ["user_id"]
  }
}
Example Call:

python
recommendations = get_personalized_recommendation(
    user_id="user_abc123",
    num_recommendations=3,
    difficulty_preference="adaptive"
)
# Returns: {
#   "recommendations": [
#     {
#       "problem_id": "contains-duplicate",
#       "relevance_score": 0.94,
#       "reason": "Targets your weakness: hash map usage...",
#       "targeted_weaknesses": ["suboptimal_time_complexity"]
#     }
#   ],
#   "weakness_summary": {"top_weaknesses": [...], "overall_readiness_score": 58}
# }
Safety Considerations:

Validate user_id exists and has sufficient attempt history (≥3 problems)
Fallback to popular problems if insufficient data for personalization
Rate limit: 50 recommendations per user per day
Cache recommendations for 5 minutes to reduce compute
A/B test recommendation algorithm variants
Allow users to flag irrelevant recommendations for model improvement
Privacy: Never expose other users' data in recommendations
Function Calling Flow
Here's how the complete function calling loop works in CodeMentor AI:

1. USER SUBMITS CODE
   ↓
2. AI DECIDES: "I need to execute this code first"
   ↓
3. AI GENERATES FUNCTION CALL (JSON)
   {
     "function": "execute_code",
     "parameters": {
       "code": "def twoSum...",
       "language": "python",
       "problem_id": "two-sum",
       "test_cases": [...]
     }
   }
   ↓
4. YOUR BACKEND EXECUTES THE FUNCTION
   - Calls Judge0 API with code + test cases
   - Waits for sandbox execution
   - Receives test results
   ↓
5. YOU RETURN FUNCTION RESULT TO AI (JSON)
   {
     "status": "completed",
     "all_passed": false,
     "test_results": [...],
     "execution_time_ms": 124
   }
   ↓
6. AI DECIDES: "Tests failed, I should analyze the code"
   ↓
7. AI GENERATES SECOND FUNCTION CALL
   {
     "function": "analyze_code_patterns",
     "parameters": {
       "user_id": "user_abc123",
       "code": "def twoSum...",
       "test_results": {...}
     }
   }
   ↓
8. YOUR BACKEND EXECUTES ANALYSIS
   - Parses AST
   - Runs ML classifier
   - Updates user weakness profile
   - Returns detected patterns
   ↓
9. YOU RETURN ANALYSIS RESULT TO AI
   {
     "detected_patterns": [
       {"pattern_type": "missing_edge_case", "confidence": 0.78, ...}
     ]
   }
   ↓
10. AI SYNTHESIZES FINAL RESPONSE
    "I see the issue! Your code doesn't handle empty arrays.
     When the input is [], your loop tries to access nums[0]
     which causes an IndexError. Here's how to fix it..."
    ↓
11. USER SEES: Natural language explanation + code suggestions
Critical Implementation Notes
The LLM Does NOT Execute Your Code

The LLM only generates function calls as JSON
Your FastAPI backend must parse the JSON and execute the actual functions
You send results back to the LLM for interpretation
Multi-Step Function Calls

The AI may chain multiple functions: execute → analyze → recommend
Your backend must support iterative function calling
Each function result informs the next function call
Error Handling

If a function fails, return error JSON to the AI
The AI will explain the error to the user naturally
Example: "I couldn't execute your code because the syntax is invalid. Let me help you fix line 5..."
Function Call Format (What You'll Receive from LLM)

json
{
  "id": "call_abc123",
  "type": "function",
  "function": {
    "name": "execute_code",
    "arguments": "{\"code\": \"def twoSum...\", \"language\": \"python\", ...}"
  }
}
Integration Checklist
 Implement FastAPI endpoints for each function
 Connect execute_code to Judge0/Piston API
 Build AST parser for Python (week 5)
 Train ML classifier for pattern detection (week 7)
 Implement recommendation algorithm (week 10)
 Add function call parser in backend
 Test function chaining (execute → analyze → recommend)
 Add rate limiting per function
 Implement error handling for failed function calls
 Log all function calls for debugging
 Create mock functions for frontend development
 Write unit tests for each function
 Document API endpoints for team
Future Functions (Post-MVP)
These functions are out of scope for the capstone but could be added later:

get_user_progress(user_id) - Retrieve detailed progress metrics for dashboard
save_code_snapshot(user_id, problem_id, code) - Save work-in-progress code
compare_with_peers(user_id, problem_id) - Anonymous benchmarking
schedule_mock_interview(user_id, difficulty) - Book timed practice session
flag_incorrect_analysis(attempt_id, feedback) - User reports wrong pattern detection
generate_hint(problem_id, current_code, hint_level) - Progressive hints without giving away solution
Questions for Team Discussion
Should analyze_code_patterns be called automatically after every execution, or only when AI determines it's needed?
Do we want users to manually request recommendations, or auto-show them after completing a problem?
Should the AI explain why it's calling a function (transparency) or keep it seamless?
How do we handle cases where the ML model is uncertain (confidence < 0.6)?
Should we implement a "skip this recommendation" feature?
Document Version: 1.0
Last Updated: November 6, 2025
Next Review: Week 8 (after first user testing)

