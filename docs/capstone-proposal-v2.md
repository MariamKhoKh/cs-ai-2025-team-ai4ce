# Refined Capstone Proposal (Version 2)

**Project Name:** CodeMentor AI  
**Team Name:** AI4ce  
**Team Members:** [Your team members]  
**Date:** Week 4, October 25, 2025  
**Version:** 2.0 (Updated from Week 2 submission)

---

## Document Change Log

### What Changed Since Week 2?

| Section | Change Type | Summary |
|---------|-------------|---------|
| Problem Statement | **Refined** | The focus was expanded from CS students to include all candidates preparing for interviews. |
| Technical Architecture | **Major Update** | Switched from custom ML to hybrid approach (GPT-4 + simple classifier) |
| Success Criteria | **Enhanced** | Added measurable metrics with specific targets |
| Risk Assessment | **Expanded** | Added 3 new risks discovered during prototyping |
| Timeline | **Realistic** | Adjusted based on Week 3-4 velocity and code execution complexity |

---

## 1. Problem Statement (Updated)

### The Problem

**Original (Week 2):**
> Many cs students fail technical interviews because they have blind spots they don't recognize.

**Refined (Week 4):**

candiates preparing for technical interviews face a critical problem: **they practice blindly without understanding their systematic weaknesses**. Through examining online communities, we confirmed that:

- candiates solve 50-100 LeetCode problems but keep making the same mistakes (e.g., always choosing O(n²) solutions, missing edge cases for empty arrays)
- LeetCode only shows "Accepted" or "Wrong Answer" without analyzing *why* their approach is suboptimal
- they waste time on random problems instead of targeting their actual gaps
- With only 2-3 interview attempts before 6-12 month waiting periods, inefficient practice is costly

**Why AI is the Right Solution:**

Traditional platforms are passive problem banks. AI can:
- **Analyze code patterns** beyond correctness (algorithmic thinking, edge case handling, code structure)
- **Detect recurring mistakes** across submissions to identify systematic weaknesses (e.g., "You miss null checks 80% of the time")
- **Generate personalized explanations** connecting mistakes to CS concepts
- **Adapt difficulty** dynamically based on performance

**Scope Validation (Week 3-4):**
- Code execution sandbox works (tested Judge0 API)
- Basic AST parsing functional (Python only for MVP)
- Custom ML model too complex for timeline → Switching to simpler rule-based + GPT-4 hybrid

---

## 2. Target Users (Updated)

### Primary User Persona

**User: "Alex" the CS Junior**

- **Demographics:** 20-22 years old, CS major (junior/senior), moderate coding experience (completed Data Structures & Algorithms)
- **Role/Context:** Preparing for summer internships at FAANG companies, practicing 1-2 hours daily for 8-12 weeks before interview season
- **Goals:** 
  - Identify blind spots before real interviews
  - Practice efficiently (work on weaknesses, not random problems)
  - Understand *why* solutions are suboptimal
  - Track measurable improvement
- **Pain Points:** 
  - "I solve problems but don't know if I'm actually improving"
  - "LeetCode doesn't tell me why my approach is wrong, just that it is"
  - "I run out of time even when I know the solution"
  - "I keep making the same mistakes but don't realize it"
- **Current Behavior:** Uses LeetCode, watches NeetCode videos, practices random Easy/Medium problems
- **Success Criteria:** Would use regularly if it clearly identifies 3+ recurring weaknesses and shows improvement over 2 weeks

### User Validation (Week 3-4)

**How We Validated:**
- Observed several students solving problems on LeetCode
- Posted in Discord groups, got 12 responses confirming problem

**Key Insights:**
1. **everybody** confirmed they don't know their specific weaknesses: "I just know I'm bad at interviews"
2. **everybody** said personalized problem recommendations would be "extremely valuable"
3. **they want concrete progress metrics**, not vague feedback like "good job"
4. **Time pressure is critical** - most of them mentioned running out of time more than getting wrong answers

---

## 3. Success Criteria (Updated & Measurable)

### Product Success Metrics

| Metric | Target (Week 15) | Measurement Method | Current Baseline (Week 4) |
|--------|------------------|-------------------|---------------------------|
| **Weakness Detection Accuracy** | ≥75% | User survey: "Is this weakness accurate?" after 5 problems | Not yet measured |
| **Problem Relevance** | ≥70% | Post-solve rating: "Was this helpful for my gaps?" | Not yet measured |
| **Task Completion Rate** | ≥80% | % of users who complete submit → review → next problem flow | Not yet measured |
| **Measurable Improvement** | ≥25% reduction | Users show fewer recurring errors after 10 problems vs first 5 | Not yet measured |
| **User Satisfaction** | ≥4.0/5.0 | Post-testing survey (Week 7 & 14) | Not yet measured |

### Technical Success Metrics

| Metric | Target | Measurement Method | Current Performance |
|--------|--------|-------------------|---------------------|
| **Code Execution Success** | ≥95% | % of submissions that execute without timeout/error | ~85% (Judge0 occasionally times out) |
| **Feedback Generation Time** | <10 seconds | Time from submit to feedback displayed | ~12 seconds (needs optimization) |
| **Pattern Detection Coverage** | ≥5 patterns/user | After 10 problems, detect at least 5 distinct error types | Not yet measured |
| **API Cost per Query** | <$0.10 | GPT-4 API cost tracking | ~$0.015 (tested on 20 samples) |
| **AST Parsing Success** | ≥90% | % of valid Python code successfully parsed | ~95% (works well) |

### Learning Goals (Team Level)

| Team Member | Learning Goal | Success Criteria | Progress (Week 4) |
|-------------|---------------|------------------|-------------------|
| [Name 1] | Master code execution sandboxing & security | Successfully integrate Judge0 with proper timeouts/limits | ✅ Basic integration working |
| [Name 2] | Build AST-based code analysis pipeline | Extract 10+ meaningful features from AST | ✅ Parser working, feature extraction in progress |
| [Name 3] | Implement adaptive recommendation algorithm | Users rate recommendations as "helpful" ≥70% | Not started (Week 8) |

**Why These Metrics Matter:**
- **75% accuracy** → Users trust the system (lower would destroy credibility)
- **<10s feedback** → Users won't abandon due to slowness
- **80% completion** → Core UX is usable
- **25% improvement** → Demonstrates actual learning value

---

## 4. Technical Architecture (Updated)

### Architecture Evolution

**What Changed Since Week 2:**

| Component | Week 2 Plan | Week 4 Reality | Why We Changed |
|-----------|-------------|----------------|----------------|
| **ML Model** | Custom Random Forest for error classification | Rule-based classifier + GPT-4 for explanations | Custom ML requires 500+ labeled examples; don't have time to collect/label |
| **Code Execution** | Uncertain between Judge0/Piston | Judge0 API | Tested both, Judge0 more reliable and better documented |
| **Scope** | 13 error categories | 6 core error categories | Realistic for timeline; can expand post-course |
| **Language Support** | Python + JavaScript | Python only (MVP) | JavaScript AST parsing more complex; defer to future work |
| **Database** | PostgreSQL for everything | PostgreSQL + Redis cache | Redis needed for problem recommendation performance |

### Current Architecture Diagram

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   User      │─────▶│   Frontend      │─────▶│    Backend      │
│  (Browser)  │◀─────│  (React +       │◀─────│  (FastAPI)      │
│             │      │   Monaco Editor) │      │                 │
└─────────────┘      └──────────────────┘      └─────────────────┘
                                                        │
                          ┌─────────────────────────────┼────────────────────┐
                          ▼                             ▼                    ▼
                  ┌───────────────┐          ┌──────────────────┐  ┌─────────────┐
                  │ Judge0 API    │          │  Analysis Engine │  │ PostgreSQL  │
                  │ (Code         │          │  • AST Parser    │  │ (User       │
                  │  Execution)   │          │  • Rule-Based    │  │  profiles,  │
                  └───────────────┘          │    Classifier    │  │  attempts)  │
                                             │  • Complexity    │  └─────────────┘
                                             │    Analyzer      │
                                             └──────────────────┘
                                                        │
                                          ┌─────────────┼──────────────┐
                                          ▼                            ▼
                                ┌──────────────────┐        ┌──────────────────┐
                                │  OpenAI API      │        │  Redis Cache     │
                                │  (GPT-4 for      │        │  (Problem queue, │
                                │   explanations)  │        │   recommendations)│
                                └──────────────────┘        └──────────────────┘
```

### Data Flow for Core User Action

**User Flow: Submit Solution**

```
1. User writes code in Monaco Editor
   ↓
2. User clicks "Submit"
   ↓
3. Frontend sends code + problem_id to backend
   ↓
4. Backend (FastAPI):
   a. Validates input (syntax check, timeout limits)
   b. Sends code to Judge0 API
   c. Gets execution results (pass/fail for each test case)
   d. If failed: AST parser analyzes code structure
   e. Rule-based classifier detects error patterns:
      - Check for missing edge case handling (if/else for null, empty)
      - Analyze time complexity (nested loops = O(n²))
      - Check for optimal data structure usage
   f. Store patterns in user weakness profile (PostgreSQL)
   g. Send patterns to GPT-4 for explanation generation
   h. Return to frontend: {result, patterns, explanation, next_problem}
   ↓
5. Frontend displays:
   - Test results (✓ or ✗)
   - Detected weaknesses with explanations
   - Personalized next problem recommendation
```

**Latency Budget:**

| Step | Target | Current | Status |
|------|--------|---------|--------|
| Code submission | <500ms | ~300ms | On track |
| Judge0 execution | <5s | ~6s | Sometimes slow |
| AST parsing | <500ms | ~200ms | On track |
| Pattern detection | <1s | ~800ms | On track |
| GPT-4 explanation | <3s | ~4s | Need prompt optimization |
| Database write | <200ms | ~150ms | On track |
| **Total (P95)** | **<10s** | **~12s** | Must optimize |

### Technology Stack

**Frontend:**
- React with TypeScript
- Monaco Editor (VS Code's editor component)
- Recharts for progress dashboard
- Hosting: Vercel

**Backend:**
- FastAPI (Python 3.11)
- Judge0 API for code execution
- Python `ast` module for AST parsing
- Hosting: Railway

**AI/ML:**
- GPT-4 for explanation generation (~$0.015/query)
- Rule-based classifier for pattern detection (no ML training needed initially)

**Data Storage:**
- PostgreSQL (user profiles, submission history)
- Redis (problem recommendation queue, caching)

**Why This Simplified Approach:**

| Original Plan | Simplified Approach | Rationale |
|---------------|-------------------|-----------|
| Train custom ML model on 500 examples | Rule-based classifier with 6 heuristics | Don't have time to collect/label 500 examples; rules cover 80% of cases |
| 13 error categories | 6 core categories | Realistic for MVP; can add more post-course |
| Python + JavaScript | Python only | One AST parser is enough complexity for 13 weeks |

### 6 Core Error Patterns (Simplified)

1. **Missing edge cases** (null, empty array, single element)
2. **Suboptimal time complexity** (O(n²) when O(n) possible with hash map)
3. **Wrong data structure** (array when hash map/set is better)
4. **Off-by-one errors** (range/loop boundaries)
5. **Missing input validation** (no checks for constraints)
6. **Inefficient nested loops** (can be optimized)

**Detection Logic (Rule-Based):**
```python
# Pseudocode
if no null checks and problem has nullable inputs:
    patterns.append("missing_edge_case_null")

if nested loops and problem solvable in O(n) with hash map:
    patterns.append("suboptimal_complexity")

if using list for lookup and >10 lookups:
    patterns.append("wrong_data_structure")
```

### Security & Cost Controls

**Implemented (Week 4):**
- Judge0 execution timeouts (5 seconds max)
- Memory limits (128MB per execution)
- Rate limiting (20 submissions/hour per user)
- Input validation (max code length 5000 characters)
- Cost tracking dashboard (monitors GPT-4 usage)

**Planned (Week 5-6):**
- Prompt optimization (reduce tokens from 500 to 250)
- Caching repeated explanations for same error patterns

### Known Technical Debt

1. **No automated tests** (planned Week 6)
2. **Judge0 occasionally slow** (need fallback or optimization)
3. **No monitoring/logging** (planned Week 8: Sentry)
4. **Prompts hardcoded** (should move to config file)
5. **No database backups** (planned Week 7)

---

## 5. Risk Assessment (Updated & Expanded)

### Risk Matrix

| Risk ID | Risk | Likelihood | Impact | Severity | Status |
|---------|------|------------|--------|----------|--------|
| R1 | Judge0 API unreliability | HIGH | HIGH | 🔴 CRITICAL | Monitoring |
| R2 | Pattern detection accuracy <70% | MEDIUM | HIGH | 🔴 CRITICAL | Testing |
| R3 | GPT-4 costs exceed budget | MEDIUM | MEDIUM | 🟡 HIGH | Mitigating |
| R4 | AST parsing fails on edge cases | MEDIUM | MEDIUM | 🟡 HIGH | Testing |
| R5 | Users don't find recommendations helpful | HIGH | MEDIUM | 🟡 HIGH | Will validate Week 7 |
| R6 | Scope creep (too many features) | HIGH | MEDIUM | 🟡 HIGH | Controlled |
| R7 | Team member unavailability | MEDIUM | MEDIUM | 🟢 MEDIUM | Planning |

### Critical Risks (Detailed)

#### 🔴 Risk R1: Judge0 API Unreliability

**Description:** Judge0 occasionally times out or returns errors, blocking core functionality.

**Likelihood:** HIGH (experienced 15% failure rate in testing)  
**Impact:** HIGH (no execution = app is useless)  
**Severity:** CRITICAL

**What We've Learned (Week 3-4):**
- Judge0 free tier sometimes slow (6-8 seconds)
- Occasional 503 errors during peak hours
- Some valid Python code rejected due to Judge0 restrictions

**Preventive Mitigation:**
1. **DONE:** Added retry logic (3 attempts with exponential backoff)
2. **DONE:** Implemented timeout handling with user-friendly errors
3. **PLANNED (Week 5):** Upgrade to Judge0 paid tier ($10/month, more reliable)
4. **PLANNED (Week 6):** Add fallback to Piston API if Judge0 fails

**Contingency Plan:**
- If Judge0 fails consistently: Switch entirely to Piston API (tested as backup)
- If both fail: Reduce scope to "analysis only" mode (no execution, just analyze code structure)

**Monitoring:**
- Track execution success rate daily
- Alert if success rate drops below 90%

**Owner:** [Backend Lead]  
**Next Review:** Week 5

---

#### 🔴 Risk R2: Pattern Detection Accuracy <70%

**Description:** If rule-based classifier incorrectly identifies weaknesses, users won't trust system.

**Likelihood:** MEDIUM (rules are simple but might miss nuances)  
**Impact:** HIGH (destroys user trust and product value)  
**Severity:** CRITICAL

**What We've Learned (Week 4 Testing):**
- Tested on 15 sample solutions
- Accuracy: ~65% (10/15 correct classifications)
- Common failures: Misidentifying optimal solutions as suboptimal

**Preventive Mitigation:**
1.  **PLANNED (Week 5):** Create golden set with 30 problems + solutions
2.  **PLANNED (Week 6):** Refine rules based on golden set testing
3.  **PLANNED (Week 7):** User testing - validate accuracy with real users
4.  **PLANNED (Week 8):** Add confidence scores (only show high-confidence patterns)

**Contingency Plan:**
- If accuracy remains <70%: Rely more on GPT-4 for classification (increase cost but improve accuracy)
- Add user feedback mechanism: "Was this accurate?" (use to improve rules)

**Monitoring:**
- Weekly golden set regression tests
- User feedback on accuracy

**Owner:** [ML Lead]  
**Next Review:** Week 5 (after golden set)

---

### High Priority Risks (Summary)

**🟡 R3: GPT-4 Costs Exceed Budget**
- Current: $0.015/query
- Budget: $50 total for semester
- Mitigation: Prompt optimization (Week 5), caching (Week 6), switch to GPT-3.5 if needed
- Monitoring: Daily cost dashboard

**🟡 R4: AST Parsing Fails on Edge Cases**
- Mitigation: Extensive testing (Week 5-6), graceful error handling
- Contingency: Skip analysis if parsing fails, still show execution results

**🟡 R5: Users Don't Find Recommendations Helpful**
- Mitigation: User testing Week 7 & 14
- Contingency: Simplify to "practice similar problems" instead of personalized queue

---

## 6. Research Plan (Updated)

### Questions We Need to Answer

#### Q1: What code features best predict error types?

**Status:**  In Progress (Week 4)  
**Deadline:** Week 5  
**Approach:**
1. Analyze 30 submissions from golden set
2. Test which AST features correlate with errors (nested loop depth, conditional branches, function calls)
3. Refine rule-based classifier

**Success Criteria:** Achieve 75%+ accuracy on golden set

---

#### Q2: Do users trust AI-generated feedback?

**Status:** Planned (Week 7)  
**Deadline:** Week 7 (user testing)  
**Approach:**
1. User testing: Show feedback for 3 problems
2. Ask: "Do you agree with this assessment?"
3. Measure: Agreement rate

**Success Criteria:** >70% agreement rate

---

#### Q3: What makes a problem recommendation "relevant"?

**Status:** Planned (Week 8)  
**Deadline:** Week 8  
**Approach:**
1. Test multiple recommendation strategies (similar problems, gradually harder, target weakest area)
2. A/B test with users
3. Measure: Which strategy gets higher "helpful" ratings

**Success Criteria:** Identify strategy with >70% helpfulness rating

---

## 7. User Study Plan

### Research Ethics

**IRB Status:** No IRB needed - IRB Light Checklist completed

**Consent & Privacy:**
- Verbal consent via Zoom
- Anonymized data (Participant 1, 2, etc.)
- Code submissions deleted after analysis
- No sensitive personal information collected

### User Testing Round 1: Week 7

**Participants:**
- **Sample size:** 5 CS students (juniors/seniors)
- **Recruitment:** CS department Slack, intro CS courses
- **Incentive:** $15 Starbucks gift card
- **Format:** Remote (Zoom), 45 minutes

**Testing Goals:**
1. Validate core submit → feedback → recommendation flow works
2. Measure perceived accuracy of weakness detection
3. Identify UX confusion points
4. Assess whether users would use this regularly

**Testing Tasks:**
1. Solve "Two Sum" problem (intentionally use O(n²) solution) - 10 min
2. Review feedback - do you agree? - 5 min
3. Solve recommended next problem - 10 min
4. Review progress dashboard - 5 min
5. Post-task survey - 10 min

**Data Collection:**
- Task completion rate
- Time on task
- Think-aloud observations
- Survey: Accuracy agreement, helpfulness, satisfaction (5-point scale)
- Would you use this regularly? (Yes/No)

**Success Criteria:**
- >75% task completion rate
- >70% agree weaknesses are accurate
- >3.5/5.0 satisfaction score
- At least 3 actionable insights for improvement

**Timeline:**
- Days 1-2: Recruit 5 participants
- Days 3-5: Conduct sessions
- Days 6-7: Analyze findings

**Deliverable:** User Testing Report (due end of Week 7)

### User Testing Round 2: Week 14

**Participants:** 5 NEW students  
**Goal:** Validate improvements from Round 1 worked  
**Success Criteria:** >80% completion, >4.0/5.0 satisfaction

---

## 8. Project Timeline (Realistic)

### Weekly Breakdown

| Week | Focus | Deliverables | Status |
|------|-------|-------------|--------|
| 1-2 | Planning | Proposal v1, team contract | Complete |
| 3 | Prototype | Basic code execution working | Complete |
| 4 | **Design Review** | **Proposal v2, architecture diagram, eval plan** | **In Progress** |
| 5 | Golden Set | 30 problems with solutions for testing | Planned |
| 6 | Core Features | AST analysis, pattern detection, basic recommendations | Planned |
| 7 | **User Testing 1** | Test with 5 users, collect feedback | Planned |
| 8 | Iteration | Fix issues from testing, improve accuracy | Planned |
| 9 | **Midterms** | Reduced project work this week | Planned |
| 10 | Dashboard | Progress tracking, visualization | Planned |
| 11 | **Safety Audit** | Test edge cases, security, cost controls | Planned |
| 12 | Recommendations | Personalized problem queue algorithm | Planned |
| 13 | Polish | Bug fixes, performance optimization | Planned |
| 14 | **User Testing 2** | Final validation (5 new users) | Planned |
| 15 | **Final Demo** | Presentation, video, case study | Planned |

### Critical Path

**Must Complete in Order:**
1. Week 5: Golden set → Blocks Week 6 testing
2. Week 6: Core features → Blocks Week 7 user testing
3. Week 7: User testing → Informs Week 8 improvements
4. Week 10: Dashboard → Needed for Week 14 testing

### Backup Plan (Scope Cuts)

**If we fall behind, cut in this order:**

**Priority 3: Cut First**
1. Progress dashboard visualization → Just show numbers
2. Multiple language support → Python only is fine
3. Collaborative filtering recommendations → Simple rule-based is okay

**Priority 2: Cut if Desperate**
4. Adaptive difficulty → All problems same difficulty
5. Detailed explanations → Just show error type

**Priority 1: Never Cut**
- Core submit → execute → feedback flow
- Pattern detection (even if simple)
- Basic recommendations
- User authentication

### Velocity Reality Check

**Week 3 Lessons:**
- Planned: 30 hours, complete prototype
- Actual: 25 hours, basic prototype (Judge0 integration took longer than expected)
- Lesson: Code execution is complex - need more buffer time

**Realistic Capacity:**
- Team member 1: 12 hours/week
- Team member 2: 10 hours/week
- Team member 3: 15 hours/week
- **Total: ~37 hours/week**

---

## 9. Team Health (Week 4 Check-In)

### What's Working

**Communication:** Daily Slack check-ins, quick responses  
**Technical Progress:** Prototype working, Judge0 integrated  
**Collaboration:** Pair programming 2x/week effective

### What Needs Improvement

**Testing:** No automated tests yet (allocate Week 6)  
**Documentation:** Code comments incomplete (spend 2 hours Week 5)  
**Workload:** Team member 2 has heavier course load (need cross-training)

### Updated Team Contract

**Meeting Schedule:**
- 2x/week in-person (Wed 6-8pm, Sat 10am-12pm)
- Daily async Slack check-ins

**Roles (Adjusted):**
- [Name 1]: Backend + Judge0 integration
- [Name 2]: Frontend + UX (reduced hours Week 9)
- [Name 3]: AST analysis + testing (new focus)

**Contingency for Week 9 (Midterms):**
- Frontload critical work to Week 5-8
- Cross-train on frontend (Week 5)
- Only non-blocking tasks in Week 9

---

## 10. Summary: Key Changes Since Week 2

### Problem & Solution
- **Validated problem** with 4 CS students
- **Narrowed target** to CS students preparing for FAANG interviews

### Technical Architecture
- **Simplified ML approach:** Custom model → Rule-based + GPT-4
- **Reduced scope:** 13 error types → 6 core types
- **Confirmed execution:** Judge0 API working (with occasional issues)
- **Removed JavaScript** from MVP (Python only)

### Success Metrics
- **Added specific targets** (75% accuracy, <10s latency, 4.0/5.0 satisfaction)
- **Baseline measurements** from Week 4 testing

### Risk Management
- **Identified Judge0 reliability** as #1 risk
- **Implemented rate limiting** and cost tracking
- **Created mitigation plans** for all critical risks

### Realistic Timeline
- **Adjusted for Week 3 velocity** (~25 hours actual vs 30 planned)
- **Buffer time for midterms** (Week 9)
- **Backup scope cuts** defined

---

## Review Checklist

- [x] All sections updated from Week 2
- [x] Specific changes documented with rationale
- [x] Measurable success metrics with targets
- [x] Architecture diagram included
- [x] All known risks documented
- [x] Realistic timeline based on Week 3-4 velocity
- [x] Team health assessment completed
- [ ] All team members reviewed and approved
- [ ] Proofread for typos
- [ ] Ready to submit

---

**Document Version:** 2.0  
**Last Updated:** October 25, 2025 (Week 4)  
**Next Review:** Week 7 (after user testing)