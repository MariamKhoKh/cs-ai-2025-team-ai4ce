# Capstone Proposal

**Course:** Building AI-Powered Applications  
**Team Name:** AI4ce  
**Project Title:** CodeMentor AI - Technical Interview Prep with Personalized Weakness Detection  
**Date:** October 18, 2025

---

## 1. Problem Statement

### The Problem

Students fail technical interviews not because they lack programming knowledge, but because they have **blind spots** they don't recognize. A student might consistently forget edge cases, default to inefficient algorithms, or struggle with specific data structures—but without detailed feedback, they keep making the same mistakes. Current platforms like LeetCode tell you if your solution is correct but don't analyze *how you think* or identify patterns in your mistakes.

This is a critical problem: tech companies receive thousands of applications, and students often get only 2-3 interview attempts before being rejected for 6-12 months. Without personalized feedback on their specific weaknesses, students waste time practicing random problems instead of addressing their actual gaps.

### Why AI is the Right Solution

Traditional interview prep platforms are passive problem banks. An AI solution can:
- **Analyze code patterns** beyond correctness (time complexity thinking, edge case handling, code structure)
- **Track recurring mistakes** across multiple problems to identify systematic weaknesses
- **Generate personalized problems** targeting specific gaps (not just random selection)
- **Adapt difficulty** based on performance, keeping students in optimal learning zone
- **Provide explanations** that connect to underlying CS concepts, not just "here's the answer"

### Scope

**In Scope:**
- Code submission interface with real-time execution
- AST-based code analysis to detect patterns (complexity habits, edge case handling, code structure)
- ML model to classify error types and identify recurring weaknesses
- Personalized problem recommendation engine
- Progress tracking dashboard showing improvement over time
- Multi-language support (Python, JavaScript initially)

**Out of Scope:**
- Live video interviews with AI
- System design interview prep (focus on coding problems)
- Behavioral interview questions
- Direct integration with company interview processes

**Why This Scope:**
This focuses on the most technically complex and valuable component—personalized weakness detection and adaptive learning. It's achievable in 13 weeks while demonstrating significant ML/AI engineering skills beyond simple API calls.

---

## 2. Target Users

### Primary User Persona

**User Type:** Computer Science Students Preparing for Tech Internships/Jobs

**Demographics:**
- Age: 20-24 (junior/senior undergrads, recent grads)
- Technical level: Can code but struggles with interview-specific skills
- Context: Practicing 1-2 hours daily for upcoming interviews

**Key Needs:**
1. **Personalized Feedback** - Know exactly what they're doing wrong repeatedly
2. **Efficient Practice** - Work on actual weaknesses, not random problems
3. **Conceptual Understanding** - Learn *why* their approach is suboptimal
4. **Progress Visibility** - See measurable improvement over time
5. **Interview Readiness Assessment** - Know when they're ready

**Pain Points:**
- "I practice a lot but keep making the same mistakes"
- "I don't know which problems to practice next"
- "LeetCode says 'wrong answer' but doesn't explain my thought process issue"
- "I can't tell if I'm actually improving"
- "I run out of time in interviews even though I know the solution"

---

## 3. Success Criteria

### Product Success Metrics

1. **Weakness Detection Accuracy:** ≥80% of identified weaknesses confirmed by users as "accurate"
2. **Problem Relevance:** ≥75% of recommended problems rated as "helpful for my gaps"
3. **Measurable Improvement:** Users show ≥30% reduction in identified weakness patterns after 2 weeks
4. **User Engagement:** Average 8+ problems solved per user in testing phase
5. **Interview Success (Proxy):** ≥70% of users report "feeling more confident" after using platform

### Technical Success Metrics

- **Code Analysis:** Successfully parse and analyze ≥95% of submitted code
- **Pattern Detection:** Identify ≥5 distinct error pattern types per user after 10 problems
- **Response Time:** Code execution + feedback generation \<10 seconds
- **Recommendation Quality:** A/B test shows personalized recommendations outperform random selection by ≥25% in user satisfaction

### Learning Goals

**Team Member 1:**
- Implement code execution sandbox and AST parsing pipeline
- Build ML model for error pattern classification
- Design adaptive recommendation algorithm

**Team Member 2:**
- Develop real-time code editor with execution feedback
- Create interactive progress dashboard with data visualization
- Implement prompt engineering for educational explanations

---

## 4. Technical Architecture

### System Overview

Users write code in a web-based IDE. Upon submission, code is executed in a sandboxed environment. An AST parser analyzes code structure, complexity, and patterns. An ML classifier identifies error types (e.g., "missed edge case," "suboptimal complexity," "poor variable naming"). Results are stored in a user profile, and a recommendation engine suggests next problems based on detected weaknesses. GPT-4 generates personalized explanations connecting mistakes to CS concepts.

### Architecture Diagram

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   User      │─────▶│   Frontend       │─────▶│    Backend      │
│  (Browser)  │◀─────│  (Next.js/       │◀─────│  (FastAPI/      │
│             │      │   Monaco Editor) │      │   Python)       │
└─────────────┘      └──────────────────┘      └─────────────────┘
                                                        │
                          ┌─────────────────────────────┼──────────────────┐
                          ▼                             ▼                  ▼
                  ┌───────────────┐          ┌──────────────────┐  ┌─────────────┐
                  │ Code Execution│          │  Analysis Engine │  │  PostgreSQL │
                  │   Sandbox     │          │  • AST Parser    │  │  (User      │
                  │   (Judge0 or  │          │  • Complexity    │  │   Profiles, │
                  │    Piston)    │          │    Analyzer      │  │   Attempts) │
                  └───────────────┘          │  • Pattern ML    │  └─────────────┘
                                             └──────────────────┘
                                                        │
                                          ┌─────────────┼──────────────┐
                                          ▼                            ▼
                                ┌──────────────────┐        ┌──────────────────┐
                                │  OpenAI API      │        │  Recommendation  │
                                │  (GPT-4 for      │        │  Engine          │
                                │   explanations)  │        │  (Personalized   │
                                └──────────────────┘        │   Problem Queue) │
                                                            └──────────────────┘
```

### Technology Stack

**Frontend:**
- Framework: Next.js 14 with TypeScript
- Code Editor: Monaco Editor (VS Code's editor)
- Visualization: Recharts for progress tracking
- Hosting: Vercel

**Backend:**
- Framework: FastAPI (Python 3.11)
- Code Execution: Judge0 API or Piston (sandboxed execution)
- AST Analysis: Python `ast` module for Python code, Acorn for JavaScript
- Hosting: Render or Railway

**AI/ML:**
- Primary LLM: GPT-4 for explanation generation
- Custom ML: scikit-learn for pattern classification (trained on labeled error data)
- Embeddings: text-embedding-3-small for problem similarity matching

**Data Storage:**
- Database: PostgreSQL (user profiles, submission history, progress tracking)
- Cache: Redis for fast problem retrieval

**DevOps:**
- Version Control: GitHub
- CI/CD: GitHub Actions
- Testing: pytest, Jest
- Monitoring: Sentry for error tracking

### Data Flow

1. **Problem Presentation:** User selects a problem (or receives recommendation)
2. **Code Submission:** User writes solution in Monaco Editor
3. **Execution:** Backend sends code to sandbox → returns test results
4. **Analysis Pipeline:**
   - AST parser extracts code structure (loops, conditionals, function calls)
   - Complexity analyzer estimates time/space complexity
   - Compare with optimal solution patterns
   - ML classifier identifies error type (13 categories, see below)
5. **Feedback Generation:**
   - GPT-4 receives: problem, user code, detected patterns, error type
   - Generates explanation with: what went wrong, why it matters, how to improve
6. **Profile Update:** Store attempt data, update weakness profile
7. **Recommendation:** Algorithm selects next problem targeting weakest areas
8. **Dashboard:** Real-time update of progress metrics

### AI/ML Components (Technical Complexity)

#### 1. Error Pattern Classification (Custom ML Model)

**13 Error Categories We'll Detect:**
- Edge case omissions (null, empty, negative, overflow)
- Suboptimal time complexity (O(n²) when O(n) exists)
- Suboptimal space complexity (unnecessary memory allocation)
- Incorrect data structure choice (array when hash map better)
- Off-by-one errors in loops
- Boundary condition mistakes
- Poor variable naming (impacts readability)
- Missing input validation
- Inefficient nested loops
- Recursion without base case
- Not considering problem constraints
- Hardcoding instead of generalizing
- Forgetting to handle duplicates

**Training Approach:**
- Start with ~500 labeled examples (hand-labeled from LeetCode submissions)
- Features: AST metrics, code length, cyclomatic complexity, test case pass pattern
- Model: Random Forest or XGBoost for interpretability
- Validation: 80/20 split, cross-validation

#### 2. Personalized Recommendation Engine

**Algorithm:**
```
For each user problem attempt:
  - Extract error patterns (from ML classifier)
  - Update user weakness profile (weighted recent attempts more)
  - Calculate "mastery score" per pattern type (0-100)
  
For problem recommendation:
  - Identify lowest mastery areas (bottom 3)
  - Retrieve problems tagged with those patterns
  - Filter by difficulty (start easier, increase as mastery improves)
  - Use collaborative filtering (problems that helped similar users)
  - Avoid recently attempted problems
```

#### 3. Adaptive Difficulty

- Track time-to-solve and attempts-to-correct
- If user struggling (>3 attempts), suggest easier variant
- If user breezing through (first-try solves), increase difficulty
- Target: 70% success rate (optimal learning zone per learning theory)

#### 4. Progress Prediction

- ML model predicts "interview readiness" score (0-100)
- Features: mastery scores, solve rate, time efficiency, consistency
- Trained on synthetic data + user self-reports
- Updates after each problem

---

## 5. Risk Assessment

### Technical Risks

**Risk #1: Code Execution Security**
- Likelihood: Medium
- Impact: Critical
- Mitigation: Use established sandbox APIs (Judge0/Piston), never execute user code directly on our servers, implement strict timeouts and memory limits

**Risk #2: ML Model Accuracy**
- Likelihood: High (initially)
- Impact: High
- Mitigation: Start with rule-based heuristics, gradually introduce ML, allow users to flag incorrect classifications, continuous model retraining

**Risk #3: AST Parsing Complexity**
- Likelihood: Medium
- Impact: Medium
- Mitigation: Start with Python only (simpler AST), add JavaScript later, use well-tested libraries, handle parse failures gracefully

### Product Risks

**Risk #1: Insufficient Training Data**
- Likelihood: Medium
- Impact: High
- Mitigation: Begin with 100 hand-labeled examples, use data augmentation, collect real user data after initial launch, use LLM to generate synthetic training examples

**Risk #2: User Abandonment (Too Hard/Easy)**
- Likelihood: Medium
- Impact: Medium
- Mitigation: Adaptive difficulty, user-controlled problem selection, clear progress indicators, gamification elements

### Team Risks

**Risk #1: Scope Creep**
- Likelihood: High
- Impact: High
- Mitigation: Strict MVP definition, weekly scope reviews, defer features to "future work"

**Risk #2: Technical Skill Gaps**
- Likelihood: Medium
- Impact: Medium
- Mitigation: Early spike tasks for risky components, office hours utilization, pair programming

### Safety & Ethical Risks

**Risk #1: Biased Feedback**
- Likelihood: Low
- Impact: Medium
- Mitigation: Test with diverse code styles, avoid penalizing unconventional but correct approaches, user feedback mechanism

**Risk #2: Over-Reliance on AI**
- Likelihood: Medium
- Impact: Low
- Mitigation: Emphasize AI as supplement to practice, provide resources for human mentorship, include disclaimer

---

## 6. Research Plan – What Do You Need to Learn? What Experiments Will You Run?

### Learning Objectives

Our research focuses on understanding **how code-level behaviors reveal cognitive learning gaps** in programming interview preparation. To achieve this, the team aims to learn:

1. **Extracting Cognitive Patterns from Code:**  
   Identify which AST features, structural metrics, and coding behaviors (e.g., missing base cases, nested loops, inefficient algorithms) best indicate recurring conceptual weaknesses.

2. **Classifying Mistakes Effectively:**  
   Determine the most effective feature engineering techniques and ML models (Random Forest, XGBoost, small neural networks) for accurate multi-class error classification.

3. **Measuring Learning Progress Over Time:**  
   Define metrics that best reflect improvement, such as reduced error recurrence, faster problem-solving, and simpler code structures.

4. **Generating Targeted Recommendations:**  
   Explore algorithms that connect user-specific weaknesses to problem sets through embedding-based similarity and collaborative filtering.

5. **Understanding User Behavior Patterns:**  
   Analyze how students respond to adaptive feedback — whether they follow suggested problems, revisit mistakes, or seek external explanations.

---

### Experiments

**Experiment 1 – AST Feature Extraction Validation**  
- **Goal:** Identify which AST-derived metrics correlate most strongly with error categories.  
- **Method:** Collect ~100 labeled code samples with annotated mistakes and extract 25+ AST metrics.  
- **Expected Outcome:** Top 5–8 predictive features for accurate classification.

**Experiment 2 – Model Benchmarking**  
- **Goal:** Compare ML models for multi-class mistake detection.  
- **Method:** Train Random Forest, XGBoost, and Logistic Regression models on labeled code data.  
- **Metrics:** Precision, recall, and F1-score per error type.  
- **Success Criterion:** ≥80% overall classification accuracy.

**Experiment 3 – Feedback Comprehension Test**  
- **Goal:** Evaluate if users can understand and act upon AI-generated feedback.  
- **Method:** Provide 10 users feedback on 2–3 problems, then reattempt similar ones.  
- **Measure:** Improvement rate and self-reported clarity of explanations.

**Experiment 4 – Adaptive Recommendation Validation**  
- **Goal:** Test if personalized problem recommendations accelerate skill improvement.  
- **Method:** Conduct A/B test — adaptive recommendations vs. random selection.  
- **Success Criterion:** ≥25% higher helpfulness ratings in the adaptive group.

**Experiment 5 – Longitudinal Performance Tracking**  
- **Goal:** Assess if repeated platform use reduces recurring error patterns.  
- **Method:** Track 10 users over 2 weeks, comparing initial and final mastery scores.  
- **Success Criterion:** ≥30% reduction in repeated error categories.

---

## 7. User Study Plan – How Will You Gather User Feedback?

### Objectives

The user study will assess **usability**, **feedback clarity**, and **perceived accuracy** of the system’s weakness detection and recommendation mechanisms. The main goal is to confirm that AI-driven insights genuinely help users understand and improve their coding interview performance.

---

### Methodology

**Participant Recruitment**  
- **Target:** 8–12 Computer Science students preparing for technical interviews.  
- **Recruitment Channels:** University mailing lists, Discord communities, peer groups, and hackathon networks.

**Data Collection Methods**  
- **Observation:** Monitor task flow and user interactions during problem-solving sessions.  
- **Surveys:** Administer post-session questionnaires (System Usability Scale and 5-point Likert items).  
- **Interviews:** Conduct semi-structured interviews to collect qualitative insights.  
- **Usage Logs:** Collect quantitative metrics such as time spent, submission counts, and repeated error frequency.

---

### Study Phases

**Phase 1 – Baseline Interaction (Week 8)**  
Participants solve standard problems, review AI-generated feedback, and rate its clarity and usefulness.

**Phase 2 – Iterative Use (Weeks 9–11)**  
Users continue practicing on the platform independently; the recommendation engine adapts based on their evolving weakness profiles.

**Phase 3 – Post-Study Evaluation (Week 12)**  
Conduct follow-up interviews, collect SUS scores, and compare user progress data to measure improvement and satisfaction.

---

### Feedback Focus Areas

- Clarity and understandability of detected weaknesses  
- Relevance of recommended problems  
- Usefulness of AI explanations for learning  
- Perceived improvement and confidence gain  
- Overall platform usability and satisfaction  

---

### Analysis Plan

- **Quantitative Analysis:**  
  Compute average SUS score, perceived accuracy rate, and reduction in repeated error frequency.  

- **Qualitative Analysis:**  
  Apply thematic analysis to interview data to identify common usability and interpretability issues.  

- **Triangulation:**  
  Cross-validate subjective feedback (confidence, satisfaction) with objective performance data (error reduction, completion time).

---

### Success Criteria

- ≥75% of users find the feedback clear and understandable  
- ≥70% rate recommendations as relevant to their weaknesses  
- ≥60% report feeling more confident about interviews after two weeks  
- Average **SUS score ≥70** (indicating “Good” usability)

---


## 8. Project Timeline

| Week | Focus | Deliverables | Risk Level |
|:-----|:------|:------------|:-----------|
| 2 | Planning | Proposal, team contract, repo | Low |
| 3 | Infrastructure | FastAPI scaffold, Next.js + Monaco Editor setup | Low |
| 4 | Code Execution | Integrate Judge0, test problem execution | **High** |
| 5 | AST Analysis | Build AST parser, extract basic metrics | **High** |
| 6 | Problem Database | Curate 50 problems with metadata, tagging | Medium |
| 7 | ML Model v1 | Train error classifier on initial dataset | **High** |
| 8 | User Testing #1 | Test core flow with 5 users | Medium |
| 9 | Feedback System | Integrate GPT-4 explanation generation | Medium |
| 10 | Recommendation Engine | Build personalized queue algorithm | **High** |
| 11 | Progress Dashboard | Visualizations, mastery scores | Low |
| 12 | User Testing #2 | 2-week longitudinal study (8 users) | Medium |
| 13 | Refinement | Bug fixes, ML model improvement | Medium |
| 14 | Polish & Documentation | Final UI polish, prepare demo | Low |
| 15 | **Final Demo** | Presentation, video, submission | Low |

### Critical Path Items

- **Week 4:** Code execution sandbox (needed for all subsequent features)
- **Week 5:** AST analysis (foundation for ML)
- **Week 7:** ML model (core differentiator)
- **Week 10:** Recommendation engine (ties everything together)

---

## 9. Dataset & Training Plan

### Initial Problem Set

- **Source:** Curated from LeetCode, HackerRank (public problems)
- **Size:** 50 problems covering:
  - Arrays (15), Strings (10), Hash Maps (8)
  - Trees (7), Graphs (5), Dynamic Programming (5)
- **Difficulty Distribution:** 30 Easy, 15 Medium, 5 Hard
- **Metadata per problem:**
  - Optimal time/space complexity
  - Common mistake tags
  - Related concept tags
  - Prerequisite problems

### ML Training Data

**Initial Dataset (Manual Labeling):**
- 100 real student submissions (ask permission to use)
- Label each with error type(s)
- Include optimal solution for comparison

**Data Augmentation:**
- Generate variations using GPT-4 (ask it to create common mistakes)
- Target: 500 labeled examples before training

**Continuous Learning:**
- Collect user feedback on classifications
- Retrain model monthly with new data
- A/B test model versions

---

## 10. Why This is Complex (Not Just an API Call)

**Compared to basic RAG chatbot:**
1. **Custom ML Model:** Training error classifier, not just using GPT
2. **Code Analysis:** Building AST parser and complexity analyzer
3. **Personalization:** Adaptive recommendation algorithm based on user history
4. **Execution Environment:** Safe code sandbox integration
5. **Multi-modal Analysis:** Combining code structure, execution results, and LLM reasoning
6. **Longitudinal Tracking:** User profile evolution over time
7. **Real-time Systems:** Editor integration, streaming feedback

**Estimated Complexity:**
- ~4000 lines of backend code (vs. ~500 for simple RAG)
- Custom ML pipeline (vs. just API calls)
- Real-time code execution (vs. static document retrieval)
- Complex state management (vs. stateless queries)

---

## 11. Future Work (Post-Capstone)

- **System Design Problems:** Add whiteboarding interface
- **Mock Interviews:** Timed, full interview simulation
- **Company-Specific Prep:** Learn patterns from Glassdoor interviews
- **Peer Comparison:** Anonymous benchmarking
- **Mobile App:** Practice on the go
- **Interview Booking:** Connect with human mentors for final prep
