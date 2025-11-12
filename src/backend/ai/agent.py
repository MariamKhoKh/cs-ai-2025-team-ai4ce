import os
from typing import Dict, Any
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool, content_types
from dotenv import load_dotenv
from src.backend.functions.tools import (
    analyze_code_submission,
    get_recommended_problem,
    track_user_progress
)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Define function declarations properly for Gemini
analyze_function = FunctionDeclaration(
    name="analyze_code_submission",
    description="Analyze user's code submission, run tests, detect error patterns, and provide feedback",
    parameters={
        "type": "object",
        "properties": {
            "problem_id": {
                "type": "string",
                "description": "Problem ID (e.g., 'two-sum', 'reverse-string')"
            },
            "user_code": {
                "type": "string",
                "description": "User's submitted code as a string"
            },
            "language": {
                "type": "string",
                "description": "Programming language (python or javascript)"
            },
            "user_id": {
                "type": "string",
                "description": "User identifier (default: 'user_001')"
            }
        },
        "required": ["problem_id", "user_code"]
    }
)

recommend_function = FunctionDeclaration(
    name="get_recommended_problem",
    description="Get next recommended problem based on user's weakness profile. Call this when user asks what to practice next.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier (default: 'user_001')"
            },
            "difficulty_level": {
                "type": "string",
                "description": "Desired difficulty level (easy, medium, or hard)"
            }
        }
    }
)

progress_function = FunctionDeclaration(
    name="track_user_progress",
    description="Update user's weakness profile after a problem submission",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "User identifier"
            },
            "problem_id": {
                "type": "string",
                "description": "Problem that was attempted"
            },
            "detected_patterns": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of error pattern types detected"
            },
            "time_taken_minutes": {
                "type": "number",
                "description": "Time spent on problem in minutes"
            },
            "attempts_count": {
                "type": "integer",
                "description": "Number of attempts made"
            },
            "solved_correctly": {
                "type": "boolean",
                "description": "Whether problem was solved correctly"
            }
        },
        "required": ["user_id", "problem_id", "detected_patterns", "time_taken_minutes", "attempts_count", "solved_correctly"]
    }
)

# Create Tool object with all functions
codementor_tool = Tool(
    function_declarations=[
        analyze_function,
        recommend_function,
        progress_function
    ]
)


class CodeMentorAgent:
    """AI agent that orchestrates function calling for CodeMentor"""
    
    def __init__(self):
        """Initialize the agent with Gemini model"""
        # Create model with tools
        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            tools=[codementor_tool]
        )
        self.chat = None
        
    def start_conversation(self):
        """Start a new conversation session"""
        self.chat = self.model.start_chat()
        return "CodeMentor AI is ready! How can I help you prepare for technical interviews?"
    
    def _execute_function_call(self, function_call) -> Any:
        """Execute a function call and return the result"""
        function_name = function_call.name
        function_args = dict(function_call.args)
        
        if function_name == "analyze_code_submission":
            result = analyze_code_submission(**function_args)
            return result.model_dump()
        elif function_name == "get_recommended_problem":
            result = get_recommended_problem(**function_args)
            return result.model_dump()
        elif function_name == "track_user_progress":
            result = track_user_progress(**function_args)
            return result.model_dump()
        else:
            return {"error": f"Unknown function: {function_name}"}
    
    def send_message(self, user_message: str) -> str:
        """
        Send a message and handle function calling manually.
        
        Args:
            user_message: User's input message
            
        Returns:
            AI's response as a string
        """
        if not self.chat:
            self.start_conversation()
        
        try:
            response = self.chat.send_message(user_message)
            
            # Check if the model wants to call a function
            while response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                
                print(f"🔧 Calling function: {function_call.name}")
                
                # Execute the function
                function_result = self._execute_function_call(function_call)
                
                # Send the function result back to the model
                response = self.chat.send_message(
                    content_types.to_content({
                        "function_response": {
                            "name": function_call.name,
                            "response": function_result
                        }
                    })
                )
            
            return response.text
        
        except Exception as e:
            import traceback
            print(f"Full error: {traceback.format_exc()}")
            return f"Error processing message: {str(e)}"
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Manually execute a function (for testing).
        
        Args:
            function_name: Name of function to call
            arguments: Function arguments as dict
            
        Returns:
            Function result
        """
        if function_name == "analyze_code_submission":
            return analyze_code_submission(**arguments)
        elif function_name == "get_recommended_problem":
            return get_recommended_problem(**arguments)
        elif function_name == "track_user_progress":
            return track_user_progress(**arguments)
        else:
            raise ValueError(f"Unknown function: {function_name}")


# Convenience function for simple usage
def chat_with_codementor(message: str, agent: CodeMentorAgent = None) -> tuple[str, CodeMentorAgent]:
    """
    Simple interface for chatting with CodeMentor.
    
    Args:
        message: User's message
        agent: Existing agent (or None to create new one)
    
    Returns:
        Tuple of (response, agent) for continued conversation
    """
    if agent is None:
        agent = CodeMentorAgent()
        agent.start_conversation()
    
    response = agent.send_message(message)
    return response, agent


if __name__ == "__main__":
    # Quick test
    print("CodeMentor AI Test\n")
    
    agent = CodeMentorAgent()
    agent.start_conversation()
    
    # Test message
    print("User: What problem should I practice next?")
    response = agent.send_message("What problem should I practice next?")
    print(f"Agent: {response}\n")
    
    # Test direct function call
    print("Direct function test:")
    result = agent.execute_function(
        "get_recommended_problem",
        {"user_id": "user_001", "difficulty_level": "easy"}
    )
    print(f"Result: {result.model_dump_json(indent=2)}")