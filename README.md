# CodeMentor AI

**Team Name:** AI4ce  
**Course:** Building AI-Powered Applications  
**Semester:** Fall 2025

## Team Members

| Name                 | Email                                  | GitHub Username | Primary Role   |
| -------------------- | -------------------------------------- | --------------- | -------------- |
| Tinatin Javakhadze   | Javakhadze.Tinatin@kiu.edu.ge         | @tjavakhadze    | Backend Lead   |
| Gvantsa Tchuradze    | Tchuradze.gvantsa@kiu.edu.ge          | @Gvantsa21      | Frontend Lead  |
| Davit Karoiani       | Karoiani.Davit@kiu.edu.ge             | @D13Karo        | AI Integration |
| Mariam Khokhiashvili | Khokhiashvili.mariam@kiu.edu.ge       | @MariamKhoKh    | Fullstack      |

---

## Project Overview

CodeMentor AI helps people prepare for technical interviews by analyzing their code submissions and identifying patterns in their mistakes. Instead of just saying "wrong answer," we detect specific weaknesses (like missing edge cases or inefficient algorithms) and recommend problems to fix those gaps.

See [docs/capstone-proposal.md](docs/capstone-proposal.md) for full project details.

---

## Current Status

### ✅ What's Working

**Core Features:**
- Code analysis with pattern detection (13 error types)
- Personalized problem recommendations based on weaknesses
- Progress tracking and mastery scoring
- Multi-language support (Python, JavaScript)

**Performance:**
- Average latency: 0.13s (59% improvement from baseline)
- Cost optimization: $0.002 per query (75% reduction)
- Cache hit rate: 32%
- Accuracy: 86% on golden set tests

**Safety & Quality:**
- 50-query golden set for testing
- Automated regression tests
- 80% resistance to prompt injection attacks
- No PII logging, clear data retention policy

### ⚠️ Known Issues

- Error rate at 14% (target: <5%) - mainly pattern detection gaps
- Some advanced algorithms not detected (sliding window, Floyd's, etc.)
- Minor bias in feedback language tone (being addressed)

---

## Recent Updates

### Week 10: Evaluation & Safety Audit (Dec 16)

Added systematic quality measurement and security testing:

- **Golden Set:** 50 test queries covering all use cases
  - 40% easy, 40% medium, 20% hard
  - Includes edge cases and adversarial inputs
- **Regression Tests:** Automated testing with quality gates
- **Safety Audit:** Red team testing, bias evaluation, privacy review
- **Monitoring:** Telemetry plan with alerts and incident response

### Week 9: Cost Optimization (Dec 9)

Optimized inference costs while maintaining quality:

- **Response Caching:** 32% hit rate, 5-minute TTL
- **Token Reduction:** Shortened prompts from 500 → 200 tokens
- **Dual Model Routing:** Use cheaper model for simple tasks
- **Results:** 75% cost reduction, 59% latency improvement

### Week 6–7: Architecture & Agent Implementation

Major improvements to system architecture and AI logic:

- Implemented Gemini 2.0 Flash function calling
- Built 3 core functions: analyze, recommend, track
- Added Pydantic validation for all inputs/outputs
- Created comprehensive error handling
- See [docs/design-review.md](docs/design-review.md) for details

---

## Tech Stack

**AI/ML:**
- Gemini 2.0 Flash (primary model)
- Gemini 1.5 Flash (for simple queries)
- Function calling for agent orchestration

**Backend:**
- Python 3.13.7
- Pydantic for validation
- Mock data (PostgreSQL planned)

**Frontend:**
- React (in development)
- Currently using CLI for testing

**Testing:**
- pytest
- Custom regression test suite
- 50-query golden set

---

## Getting Started

### Prerequisites

```bash
# Python 3.13+
python --version

# Install dependencies
pip install google-generativeai pydantic python-dotenv pytest tenacity --break-system-packages
```

### Setup

1. **Clone the repo**
```bash
git clone https://github.com/your-org/codementor-ai.git
cd codementor-ai
```

2. **Set up environment**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
```

3. **Run tests**
```bash
# Unit tests
pytest tests/test_functions.py -v

# Regression tests
python tests/test_regression.py
```

4. **Try it out**
```bash
# Start agent
python src/backend/ai/optimized_agent.py

# Ask questions like:
# "What problem should I practice next?"
# "Analyze this code: def two_sum(nums, target): ..."
```

---

## Testing

### Running Regression Tests

```bash
cd tests/
python test_regression.py

# Expected output:
# - 50 queries tested
# - Accuracy: 86%
# - Latency: 0.13s average
# - Error rate: 14%
```

### Current Test Results

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Accuracy | 86% | ≥ 80% | ✅ PASS |
| Avg Latency | 0.13s | ≤ 3.0s | ✅ PASS |
| P95 Latency | 0.18s | ≤ 5.0s | ✅ PASS |
| Avg Cost | $0.002 | ≤ $0.25 | ✅ PASS |
| Error Rate | 14% | ≤ 5% | ❌ NEEDS WORK |

---


December 16, 2024*
