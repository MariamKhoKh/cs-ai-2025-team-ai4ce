# Architecture Decision: Agent vs Direct Function Calling

## Decision: **Direct Function Calling (Recommended)**

## Justification

CodeMentor uses **direct function calling** rather than a full ReAct agent because:

1. **Predictable Flow**: Our use cases follow deterministic paths:
   - User submits code → Analyze → Return feedback
   - User asks "what next?" → Check weaknesses → Recommend problem
   - User completes problem → Update progress → Show stats

2. **Cost Efficiency**: Direct function calls are 3-5x cheaper than multi-step agent reasoning. For a student-facing app, keeping costs under $0.10/session is critical.

3. **Latency**: Function calls return results in 1-2 seconds vs 5-10 seconds for agent loops. Interview prep requires immediate feedback.

## When Would We Need an Agent?

We would switch to an agent if we added features like:
- "Create a personalized 30-day study plan" (requires multi-step planning)
- "Research this algorithm and find related problems" (requires iterative web search)
- "Debug my code by trying different approaches" (requires experimentation loop)

## Current Architecture

```
User Query → Gemini decides which function → Execute function → Return result
```

No ReAct loop needed because Gemini's function calling is sufficient for our single-step tasks.