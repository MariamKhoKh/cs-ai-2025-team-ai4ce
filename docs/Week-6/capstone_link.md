Capstone Project Link - Lab 6
Project: CodeMentor AI - Technical Interview Prep with Personalized Weakness Detection
Team: AI4ce
Date: November 11, 2025

How Lab 6 Functions Connect to Capstone
Lab 6's three functions (analyze_code_submission, get_recommended_problem, track_user_progress) form the core intelligence layer of the CodeMentor AI capstone. They enable the AI to:

Understand what the user struggles with (code analysis + pattern detection)
Recommend personalized practice problems (adaptive learning)
Track improvement over time (progress dashboard)
Without these functions, the capstone would just be a static problem bank. With them, it becomes an adaptive, AI-powered interview coach that learns from each submission.

Primary Function for Capstone: analyze_code_submission()
Why This Function is Critical:

This function is the heart of the capstone because it bridges the gap between:

What the user submits (raw code)
What the AI understands (error patterns, weaknesses)
What the user learns (actionable feedback)
It's the only function that processes user input in real-time and generates value immediately. The other two functions depend on this one's output to work.

Current Implementation (Week 6 - Mock Data):

python
def analyze_code_submission(problem_id, user_code, language):
    # 1. Run hardcoded test cases
    # 2. Detect patterns via rule-based checks
    # 3. Generate AI feedback via LLM
    # 4. Return structured response (CodeAnalysisResponse)
Next Steps for Capstone Integration:

Week 7: Real Code Execution
Replace mock tests with Judge0 API - Execute user's code in sandboxed Docker container
Dynamic test case loading - Fetch test cases from database based on problem_id
Real-time performance metrics - Measure actual execution time and memory usage
Estimated Effort: 8-10 hours
Blocker Risk: Medium (Judge0 API might be slow or unreliable - need fallback to local sandbox)

Week 8: ML-Powered Pattern Detection
Train a classifier - Use labeled dataset of 500+ submissions with known error patterns
Replace rule-based detection - Current version uses if-statements; upgrade to scikit-learn RandomForest
Confidence scores - Return probability for each detected pattern (e.g., "85% likely off-by-one error")
Estimated Effort: 12-15 hours
Blocker Risk: High (need to collect/label training data - might use synthetic data generation)

Week 9: Database Persistence
Store all submissions - PostgreSQL table with columns: submission_id, user_id, problem_id, code, timestamp, result
Query historical patterns - "Show me all times this user made off-by-one errors"
Enable progress trends - Track mastery score over time (currently only stored in memory)
Estimated Effort: 6-8 hours
Blocker Risk: Low (standard CRUD operations, well-documented)

Week 10: Frontend Integration
Monaco Editor - Replace text input with full-featured code editor (syntax highlighting, auto-complete)
Live feedback display - Show test results as user types (debounced to avoid API spam)
Visual progress charts - Use Recharts to display weakness trends from track_user_progress()
Estimated Effort: 10-12 hours
Blocker Risk: Medium (React state management for real-time updates can be tricky)

Success Metrics for Capstone
By the final demo (Week 12), analyze_code_submission() should:

Accuracy: Detect error patterns with ≥80% precision (compared to manual labeling)
Speed: Return feedback in <3 seconds (including Judge0 execution time)
Usefulness: ≥70% of beta testers say feedback helped them improve (user survey)
Reliability: Handle 50 concurrent submissions without crashing (load testing)
Capstone Dependencies on Lab 6
Capstone Feature	Lab 6 Function	Why It's Essential
Real-time Code Feedback	analyze_code_submission()	Without this, users can't submit code or get feedback
Personalized Problem Queue	get_recommended_problem()	Without this, users see random problems (no adaptive learning)
Progress Dashboard	track_user_progress()	Without this, users can't see improvement trends (low retention)
Weakness Heatmap	All three functions	Combines data to show which patterns user struggles with most
Interview Readiness Score	track_user_progress()	Overall metric to tell user if they're ready for real interviews
Risk Mitigation
What if Judge0 API is too slow or expensive?

Fallback Plan: Self-host Judge0 using Docker Compose on AWS EC2
Cost Estimate: ~$30/month for t3.medium instance (vs. $100+/month for API at scale)
What if pattern detection accuracy is poor?

Fallback Plan: Use GPT-4 to analyze code and extract patterns (slower but more accurate)
Hybrid Approach: Use ML classifier as first pass, then GPT-4 for low-confidence cases
What if we can't collect enough training data?

Fallback Plan: Generate synthetic data using LLM (prompt: "Write 50 Python solutions to Two Sum with off-by-one errors")
Commitment to Capstone
I will prioritize analyze_code_submission() in all upcoming weeks because:

It's user-facing and high-impact (visible in every demo)
It's technically challenging (good for learning)
It's the foundation for all other features
Weekly Time Allocation (Weeks 7-12):

50% on analyze_code_submission() improvements
30% on supporting functions (database, frontend)
20% on testing and documentation
Reflection
Lab 6 transformed the capstone from a vague idea into working software. Seeing the functions actually return structured data and integrate with the AI agent made the project feel real. The Pydantic models forced me to think carefully about data shapes, which will make future database design easier.

Biggest Challenge: Balancing mock data simplicity with future integration complexity. I designed the functions to work with mocks now but also anticipate real Judge0/PostgreSQL later.

Biggest Success: Multi-turn conversations work perfectly. The AI can analyze code, recommend a problem, track progress, and then seamlessly continue the conversation. This proves the core loop is solid.

Next Milestone: Week 7 demo should show a user submitting real Python code that executes in Judge0 and returns actual test results (not mocks). That's when the capstone truly comes alive.

