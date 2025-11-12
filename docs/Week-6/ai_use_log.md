AI Use Log - Lab 6: Function Calling & Structured Outputs
Project: CodeMentor AI
Team: AI4ce
Date: November 11, 2025

AI Tools Used
1. Claude (Anthropic) - Primary Development Assistant
Purpose: Architecture design, code generation, debugging, and documentation

Specific Tasks:

Pydantic Model Design - Generated the three main model classes (CodeAnalysisResponse, RecommendationResponse, ProgressTrackingResponse) with proper field types, descriptions, and validation rules
Function Implementation - Created skeleton code for analyze_code_submission(), get_recommended_problem(), and track_user_progress() with mock data logic
Test Suite Creation - Generated pytest test cases covering basic functionality, edge cases, error handling, and multi-turn conversation flows
Documentation Writing - Drafted README.md and this week's implementation overview with clear structure and examples
Error Handling Patterns - Suggested try-except blocks and user-friendly error messages for all functions
Code Review - Reviewed my initial implementations and suggested improvements (e.g., adding max_length validation to prevent abuse)
Prompts Used:

"Create Pydantic models for a code analysis function that returns test results, detected error patterns, and AI feedback"
"Write pytest tests for a recommendation function that suggests coding problems based on user weaknesses"
"How should I structure error handling for LLM function calls that might fail?"
Code Generated: ~60% of the codebase structure, heavily edited and customized for our specific use case

2. GitHub Copilot - Code Completion
Purpose: Auto-completion while typing, boilerplate reduction

Specific Tasks:

Type Hints - Suggested proper Python type annotations (e.g., List[ErrorPattern], Literal["python", "javascript"])
Docstrings - Generated Google-style docstrings for functions based on function signatures
Mock Data - Completed mock user profiles and test case data after I started typing the structure
Import Statements - Auto-suggested correct imports for Pydantic, typing, datetime
Test Assertions - Completed assert statements in pytest based on expected outcomes
Code Generated: ~20% of the codebase (mostly repetitive boilerplate and data structures)

3. ChatGPT (OpenAI) - Research & Conceptual Questions
Purpose: Understanding concepts, best practices research

Specific Tasks:

Function Calling Schemas - Asked how to convert Pydantic models to OpenAI function calling JSON schema format
LLM Prompt Engineering - Researched best practices for getting structured outputs from Gemini API
Error Pattern Taxonomy - Discussed common coding error categories for technical interviews (off-by-one, edge cases, time complexity issues)
Testing Strategy - Asked about pytest best practices for AI-powered functions
Prompts Used:

"What are the most common coding error patterns in technical interviews?"
"How do I convert a Pydantic model to OpenAI function calling schema?"
"Best practices for testing functions that call LLM APIs?"
Code Generated: 0% (only provided conceptual guidance and examples)

AI-Assisted vs. Human-Written Breakdown
Component	AI-Assisted %	Human-Written %	Notes
Pydantic Models	70%	30%	Claude generated base structure, I added validation rules and descriptions
Function Logic	50%	50%	Claude created skeletons, I implemented project-specific business logic
Test Cases	60%	40%	Copilot completed assertions, I designed test scenarios
Mock Data	80%	20%	AI generated data structures, I customized values for realism
Documentation	40%	60%	AI drafted templates, I added project-specific details and context
Error Handling	50%	50%	Claude suggested patterns, I adapted for our use cases
What AI Did Well
✅ Speed: Reduced development time by ~40% by generating boilerplate code
✅ Best Practices: Suggested proper Pydantic validation patterns I wasn't aware of
✅ Documentation: Created clear docstrings and README structure
✅ Test Coverage: Thought of edge cases I initially missed (e.g., empty code submission)
✅ Error Messages: Generated user-friendly error text (I tend to write technical error messages)

What Required Human Oversight
⚠️ Business Logic: AI couldn't infer our specific weakness tracking algorithm (mastery score calculation)
⚠️ Mock Data Realism: AI-generated test cases were too simple (e.g., "test1", "test2" - I made them realistic)
⚠️ Integration Flow: AI suggested each function independently, I had to design how they work together
⚠️ Project Context: AI didn't know our capstone goals, so I had to guide it toward technical interview prep focus
⚠️ Security: AI didn't flag input length limits - I added max_length=10000 after thinking about abuse cases

Lessons Learned
AI as a Partner, Not a Replacement: Works best when I clearly specify requirements, then AI generates implementation. Still need to review every line.
Iterative Refinement: First AI draft is ~70% correct. Usually needs 2-3 rounds of "now add X" or "change this to Y" to get production-ready code.
Explain the "Why": When AI generates something I don't understand, I ask it to explain. Learned about Pydantic's Field() validation this way.
Cross-Verify: Used multiple AI tools (Claude + ChatGPT) to verify best practices. When they agree, it's probably correct.
Test Everything: Even though AI wrote test cases, I ran them to make sure they actually work. Found 2 failing tests due to incorrect assumptions.
Ethical Considerations
Academic Honesty: All AI-generated code was reviewed, understood, and modified by me. I can explain every line if asked.
Attribution: This log documents AI usage transparently as required by the syllabus.
Learning: Used AI to accelerate learning, not replace it. Studied concepts AI introduced (e.g., Pydantic validators).
Originality: The overall architecture, project vision, and integration strategy are 100% human-designed. AI helped implement, not design.
Future AI Use
For Week 7+ (database integration and Judge0), I plan to:

Use Claude to generate SQL migration scripts (with manual review)
Ask ChatGPT about Judge0 API security best practices
Use Copilot for boilerplate database models
Continue documenting all AI usage in this log
Conclusion
AI tools significantly accelerated Week 6 implementation, cutting development time from ~6 hours to ~3.5 hours. However, human judgment was essential for:

Ensuring code quality and security
Maintaining project vision and goals
Verifying correctness through testing
Adapting generic solutions to our specific use case
The combination of AI speed and human oversight resulted in production-ready code that meets all Lab 6 requirements.

