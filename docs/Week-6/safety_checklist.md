Safety Checklist - Lab 6: CodeMentor AI
Project: CodeMentor AI
Team: AI4ce
Date: November 11, 2025

✅ API Key Security
 API keys stored in .env file only - Never hardcoded in source code
 .env file added to .gitignore - Prevents accidental commits to GitHub
 .env.example provided - Shows required variables without exposing actual keys
 Environment variables loaded via python-dotenv - Secure access pattern
 No API keys in commit history - Verified with git log -p | grep -i "api_key"
 Instructions in README - Team members know how to set up their own keys
Evidence: All API key access uses os.getenv("GEMINI_API_KEY"), never string literals.

✅ Data Privacy
 No real user data in Week 6 - All data is mock/synthetic
 User IDs are anonymized - Default to generic IDs like "user_001"
 No PII in test cases - Test data uses fake names and generic identifiers
 Code submissions are temporary - Not persisted to disk or logs (mock phase)
 Planned database security - Will use parameterized queries to prevent SQL injection (Week 7+)
Current Data Flow: User input → Function validation → Mock data response → Discarded (no persistence)

Future Considerations:

Add user authentication before storing real submissions
Encrypt sensitive data at rest (PostgreSQL with encryption)
Implement data retention policy (auto-delete after 90 days)
✅ Input Validation & Sanitization
 Pydantic models enforce types - All function inputs validated before execution
 Language restricted to whitelist - Only "python" and "javascript" allowed
 Problem IDs validated - Must match known problem format
 Code length limits - Maximum 10,000 characters to prevent abuse
 No code execution in Week 6 - Mock phase uses hardcoded test results
 Special characters handled - String inputs escaped in AI prompts
Example Validation:

python
class CodeSubmissionRequest(BaseModel):
    problem_id: str = Field(pattern="^[a-z0-9-]+$")
    user_code: str = Field(max_length=10000)
    language: Literal["python", "javascript"]
Future (Judge0 Integration):

Use sandboxed execution environment (Judge0 Docker containers)
Set time limits (5 seconds max) to prevent infinite loops
Set memory limits (256MB) to prevent resource exhaustion
Block dangerous system calls (file I/O, network access)
✅ Error Handling
 All functions wrapped in try-except - No unhandled exceptions crash the app
 User-facing error messages - Technical details hidden, friendly messages shown
 Validation errors caught - Pydantic errors return clear guidance
 Fallback responses - If AI generation fails, return default helpful message
 Logging for debugging - Errors logged to console (will use proper logger in production)
Error Handling Pattern:

python
try:
    result = analyze_code_submission(...)
except ValidationError as e:
    return {"error": "Invalid input. Please check your code format."}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": "Something went wrong. Please try again."}
✅ AI Model Safety
 Prompt injection prevention - User code wrapped in delimiters, not directly interpolated
 Output validation - AI responses parsed and validated before returning to user
 Temperature set appropriately - 0.7 for feedback (creative but not random)
 Max tokens limited - Prevents extremely long responses that could be abusive
 Content filtering planned - Will add profanity check in Week 7
 Fallback if AI fails - Returns generic feedback if LLM call times out
Prompt Structure:

Analyze the following code submission.
USER CODE (DO NOT EXECUTE):
---
{user_code}
---
Provide constructive feedback only. Do not generate harmful content.
Future Enhancements:

Add content moderation API to check AI responses
Implement rate limiting to prevent abuse
Monitor for inappropriate prompts and block repeat offenders
✅ Code Execution Safety (Future)
Current Status (Week 6): No real code execution - all results are mocked.

Planned for Judge0 Integration (Week 7+):

 Research completed - Judge0 uses Docker containers for sandboxing
 Use Judge0 API (not self-hosted) - Avoid managing security ourselves
 Set strict resource limits - 5 sec timeout, 256MB memory
 Disable network access - Containers cannot make external requests
 Block file system access - Code cannot read/write files
 Whitelist languages - Only Python and JavaScript allowed
 Rate limit submissions - Max 10 per user per minute
✅ Dependency Security
 All dependencies pinned - requirements.txt uses exact versions
 No known vulnerabilities - Checked with pip-audit (Week 6 snapshot clean)
 Minimal dependencies - Only essential packages installed
 Official sources only - All packages from PyPI official repository
Dependencies:

openai==1.12.0 - Official OpenAI/Gemini SDK
pydantic==2.6.0 - Input validation
python-dotenv==1.0.0 - Environment variable management
pytest==8.0.0 - Testing (dev only)
Future: Set up Dependabot to auto-update dependencies with security patches.

✅ GitHub & Version Control
 .gitignore configured - Excludes .env, __pycache__, venv/
 No secrets in commit history - Verified with git log -p
 Clear commit messages - Describes changes without exposing implementation details
 Branch protection planned - Will require PR reviews for main branch (Week 8+)
✅ Deployment Readiness (Future)
Not Yet Deployed - Planning Checklist:

 Use environment-specific configs (dev/staging/prod)
 Enable HTTPS only (no plain HTTP)
 Add rate limiting (e.g., 100 requests/hour per user)
 Implement monitoring (log errors to service like Sentry)
 Set up automated backups (daily PostgreSQL snapshots)
 Add health check endpoint (/health)
 Use secrets manager (AWS Secrets Manager or similar)
Summary
Current Safety Score: 9/10 (Excellent for Week 6 mock phase)

Strengths:

Strong input validation with Pydantic
Secure API key management
Comprehensive error handling
No code execution risk (mock data)
Areas to Address (Week 7+):

Real code execution security (Judge0 sandboxing)
Database security (parameterized queries, encryption)
Content moderation for AI responses
Rate limiting for API calls
Conclusion: The Week 6 implementation is safe for development and testing. All critical security measures are in place for the mock data phase. Before production deployment, we will implement the remaining items in the "Future" sections above.

