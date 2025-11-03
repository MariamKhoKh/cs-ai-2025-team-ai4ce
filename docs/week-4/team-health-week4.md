# Team Health Check - Week 4

**Team Name:** AI4ce  
**Team Members:** Mariam Khokhiashvili, Tinatin Javakhadze, Gvantsa Tchuradze, Davit Karoiani  
**Date:** Week 4, October 26, 2025

---

## Quick Health Check

| Category | Rating (1-5) | Notes |
|----------|--------------|-------|
| **Communication** | 4/5 | Regular check-ins established, clear channels |
| **Collaboration** | 4/5 | Good knowledge sharing and support |
| **Technical Progress** | 4/5 | On schedule with core infrastructure tasks |
| **Workload Balance** | 4/5 | Contributions distributed evenly across team |
| **Morale** | 4/5 | Team engaged and motivated |
| **Confidence in Success** | 4/5 | Clear path to MVP, manageable risks identified |

**Overall Team Health:** 4/5 - Strong foundation established

---

## What's Working Well

### Communication
- **Daily async check-ins** keeping everyone aligned without excessive meetings
- **Clear documentation practices** making it easy to understand each component
- **Responsive on Slack/Discord** - questions get answered within a few hours

### Technical Collaboration
- **Code reviews are educational** - team members learning from each other's approaches
- **Good balance of independent work and collaboration** - people know when to ask for help
- **Technical decisions are documented** in `/docs` for transparency

### Task Management
- **Backlog prioritization is clear** - no confusion about what to work on next
- **GitHub Projects board** provides good visibility into progress
- **Weekly sync meetings** keep everyone on same page

---

## What Needs Improvement

### Improvement 1: Enhanced Testing Strategy

**Description:** As we build core features, we need a clearer approach to testing to ensure quality and catch issues early.

**Impact:** Better test coverage will prevent bugs from reaching user testing and make iteration faster.

**Proposed Solution:**
- Establish testing conventions for unit tests (>80% coverage target)
- Add integration test examples to `/docs/testing-guide.md`
- Dedicate 20% of development time to writing tests alongside features

**Owner:** Team to discuss and establish conventions

**Target Date:** Week 5 (testing guide completed)

---

### Improvement 2: Cross-Training on Components

**Description:** Each team member has primary ownership of certain components. Building shared knowledge would make the team more resilient.

**Impact:** Reduces single points of failure and enables team members to assist each other more effectively.

**Proposed Solution:**
- Brief component overviews (15 min) in weekly meetings
- Pair programming sessions when tackling complex features
- Rotate code review assignments to expose everyone to different parts of the system

**Owner:** Team lead to schedule component overview sessions

**Target Date:** Ongoing starting Week 5

---

### Improvement 3: Documentation Timing

**Description:** Technical documentation is being written but sometimes after features are already merged, making it harder for others to understand.

**Impact:** Small delay in team members understanding new components; not critical but could be optimized.

**Proposed Solution:**
- Include documentation checklist in PR template
- High-level architecture docs written before implementation
- Code comments for complex logic added during development

**Owner:** Everyone follows documentation standards

**Target Date:** Week 5 (update PR template)

---

## Individual Check-Ins

### Backend Lead: [Name]

**Role:** Backend architecture, API development, database design

**Current Tasks:**
- Issue #1: Code Execution Sandbox
- Issue #2: Problem Database Schema

**Capacity This Week:** 3/5 (comfortable) - ~10 hours/week

**Blockers:**
- None currently

**Support Needed:**
- Feedback on API endpoint design would be helpful

**How They're Feeling:** "Making solid progress on infrastructure. Excited to see the pieces come together."

---

### Frontend Lead: [Name]

**Role:** React UI, code editor integration, visualization

**Current Tasks:**
- Research for Issue #3: Frontend Problem Display
- Planning Issue #11: Progress Dashboard design

**Capacity This Week:** 3/5 (comfortable) - ~10 hours/week

**Blockers:**
- Waiting for backend API contracts to finalize frontend integration

**Support Needed:**
- Example API response formats for mocking

**How They're Feeling:** "Good momentum. Ready to start building UI once backend contracts are defined."

---

### ML Lead: [Name]

**Role:** AST analysis, ML classifier, recommendation algorithm

**Current Tasks:**
- Planning Issue #4: AST Parser architecture
- Research for Issue #7a: Training data collection strategy

**Capacity This Week:** 3/5 (comfortable) - ~10 hours/week

**Blockers:**
- None currently

**Support Needed:**
- Team input on which error patterns to prioritize for initial classifier

**How They're Feeling:** "Excited about the ML components. Planning phase going well."

---

## Updated Team Contract (If Changes Needed)

### No Major Changes Needed

The Week 2 team contract is working well. Minor refinements below:

| Aspect | Week 2 | Week 4 Refinement | Reason |
|--------|--------|-------------------|--------|
| **Meeting Length** | 1 hour | 45 minutes (tighter agenda) | More efficient use of time |
| **Code Review SLA** | "Soon" | Within 24 hours | Set clear expectations |

### Current Agreements (Working Well)

**Meeting Schedule:**
- **Mon/Wed/Fri 5pm (45 min)**: Progress sync, blockers, decisions
- **Friday retrospective (last 15 min)**: What went well, what to improve

**Communication:**
- **Slack**: Daily standup updates (brief status, today's focus)
- **GitHub**: PR reviews within 24 hours, discussions in PR comments
- **Discord**: Ad-hoc pairing and screen sharing for debugging

**Roles & Responsibilities:**
- **Backend Lead**: Code execution, database, API architecture
- **Frontend Lead**: React UI, visualizations, user testing coordination
- **ML Lead**: AST analysis, ML model, recommendation algorithm
- **Shared**: Documentation, testing, problem curation

**Decision-Making:**
- Technical decisions: Component owner decides, documents rationale
- Architecture changes: Team discussion in meeting or Slack thread
- Scope changes: Team consensus required

**Conflict Resolution:**
1. Direct conversation first
2. Bring to team retrospective if unresolved
3. Office hours with instructor if needed

---

## Risk Mitigation

### Team-Level Risks

**Risk 1: Technical Integration Complexity**

**Description:** Multiple components (execution sandbox, AST parser, ML model, frontend) need to work together smoothly. Integration points could surface unexpected issues.

**Likelihood:** Medium (normal for complex systems)

**Impact:** Medium (could delay features but unlikely to block MVP)

**Mitigation Plan:**
- Integration tests for each major component interaction
- Weekly "integration checkpoint" to test end-to-end flow
- Maintain clear API contracts between components
- Build modular architecture allowing components to be tested independently

**Early Warning Signs:**
- Components work individually but fail when connected
- Repeated changes to API contracts indicating unclear requirements

**Escalation Path:**
- Schedule focused integration session to resolve issues
- Simplify integration points if necessary

---

**Risk 2: Training Data Quality**

**Description:** ML model quality depends on having well-labeled, diverse training examples. Collecting 500 quality examples is time-intensive.

**Likelihood:** Medium (ambitious data collection goal)

**Impact:** High (affects core differentiator, but fallback exists)

**Mitigation Plan:**
- Start data collection early (Week 5-6)
- Use multiple sources: GPT-4 generation, manual creation, existing datasets
- Create clear labeling guidelines to ensure consistency
- Team collaboration on labeling (distribute work)
- Fallback: Rule-based error detection if ML model quality insufficient

**Early Warning Signs:**
- Week 6: Less than 250 examples collected
- Low inter-rater agreement on error classifications

**Escalation Path:**
- Simplify error categories (reduce from 13 to 5 most common)
- Extend data collection timeline, adjust ML model scope

---

**Risk 3: User Recruitment for Testing**

**Description:** Need 5 users for Week 8 testing and 8 users for Week 12 study. University schedule and competing priorities may affect recruitment.

**Likelihood:** Low-Medium (competitive for students' time)

**Impact:** Medium (affects evaluation quality but workarounds exist)

**Mitigation Plan:**
- Start recruitment early (Week 5)
- Multiple recruitment channels: CS department, Discord, personal networks
- Clear time commitment (45 min) and incentives ($10 gift cards)
- Pilot testing with team members and friends as backup
- Flexible scheduling for participants

**Early Warning Signs:**
- Week 6: Fewer than 3 confirmed participants for Round 1
- Week 10: Fewer than 5 confirmed participants for Round 2

**Escalation Path:**
- Increase incentive amount
- Expand recruitment channels
- Use convenience sample if necessary

---

## Progress Tracking


**Trend:** Stable (establishing baseline)

**Insights:**
- Initial estimates were reasonable
- Learning curve on new technologies (Judge0, Monaco Editor) adds time
- Documentation time not always accounted for in original estimates

---

## Team Strengths

**Technical Skills:**
- **Full-stack coverage**: Backend, frontend, and ML expertise distributed across team
- **Strong foundation in core technologies**: Python, React, machine learning libraries
- **Quick learners**: Team picks up new tools (Judge0, Monaco Editor, AST parsing) efficiently
- **Good software engineering practices**: Version control, code review, documentation

**Collaboration:**
- **Respectful communication**: Team members provide constructive feedback
- **Proactive help-seeking**: People ask questions before getting stuck
- **Shared ownership mindset**: Willing to contribute outside primary areas
- **Good meeting facilitation**: Discussions stay focused and productive

**Problem-Solving:**
- **Research skills**: Team finds relevant documentation and examples efficiently
- **Pragmatic decision-making**: Balances ideal solutions with time constraints
- **Risk awareness**: Identifies potential issues early
- **Flexibility**: Willing to adjust plans based on new information

---

## Goals for Next 2 Weeks

### Team Goals
1. **Complete core infrastructure** (Issues #1-2) to enable feature development
2. **Begin training data collection** targeting 250+ examples by Week 6
3. **Establish testing conventions** and document in `/docs/testing-guide.md`
4. **Start user testing recruitment** for Week 8 study

### Individual Goals

**Backend Lead:** Complete code execution and database infrastructure; document API contracts  
**Frontend Lead:** Build problem display UI and code editor integration; create design mockups for dashboard  
**ML Lead:** Design AST analysis pipeline; create training data collection strategy and guidelines

---

## Action Items from This Check-In

- [ ] **Update PR template with documentation checklist** - Owner: Team lead - Due: Oct 28
- [ ] **Create testing conventions guide** - Owner: Everyone contributes - Due: Nov 2
- [ ] **Schedule component overview sessions (15 min each)** - Owner: Team lead - Due: Nov 1
- [ ] **Define API contracts for backend-frontend integration** - Owner: Backend + Frontend leads - Due: Oct 30
- [ ] **Draft training data labeling guidelines** - Owner: ML lead - Due: Nov 1
- [ ] **Send user testing recruitment email** - Owner: Frontend lead - Due: Nov 2

---

## ✅ Sign-Off

**All team members have reviewed and agree with this assessment**


**Date Completed:** October 26, 2025  
**Next Check-In:** Week 6 (mid-semester checkpoint)

---

**Notes:**
- Team is progressing well on foundational work
- No critical issues identified; refinements are standard process improvements
- Communication and collaboration patterns are healthy
- Risks are identified with clear mitigation strategies
- Workload is balanced across team members