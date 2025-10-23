
# Capstone Proposal

**Course:** Building AI-Powered Applications  
**Team Name:** AI4ce 
**Project Title:** KIU Bot 
**Date:** October 16, 2025

-----

## 1\. Problem Statement

### The Problem

Incoming and first-year university students are frequently overwhelmed by the sheer volume of new information they need to navigate their campus and administrative duties. At institutions like KIU, critical information is often scattered across multiple websites, dense PDF handbooks, and various departmental portals. This fragmentation makes it difficult for students to find quick, reliable answers to common but crucial questions like, "Where is the financial aid office?", "What are the add/drop deadlines?", or "How do I connect to the campus Wi-Fi?".

Currently, students resort to inefficient methods like keyword-searching the university website, asking peers who may have incomplete information, or physically going to administrative offices and waiting in long lines. These workarounds lead to frustration, wasted time, and can cause students to miss important deadlines or opportunities. This problem is particularly acute for the hundreds of new students matriculating each year, creating a significant, recurring strain on administrative staff who must answer the same questions repeatedly.

An AI-powered solution is uniquely suited to solve this problem. [cite\_start]A chatbot using Retrieval-Augmented Generation (RAG) can ingest this scattered information into a centralized, searchable knowledge base[cite: 255]. Unlike a simple keyword search, it can understand and answer questions asked in natural language, providing a conversational and accessible single source of truth. [cite\_start]This directly addresses the core issue by providing instant, 24/7 access to verified information, freeing up staff time and empowering students to be more self-sufficient[cite: 107].

### Scope

**What's In Scope:**

  - A web-based chat interface for users to ask questions.
  - A RAG pipeline that answers queries based on a curated set of official KIU documents (e.g., student handbook, course catalog, FAQ pages).
  - Citing the source document for each answer to ensure trustworthiness.

**What's Out of Scope (but maybe future work):**

  - User accounts and personalized information (e.g., "What's my class schedule?").
  - Integration with real-time university systems (e.g., checking classroom availability).
  - Transactional capabilities like booking appointments or registering for courses.

**Why This Scope Makes Sense:**
[cite\_start]This scope is focused on solving the core information retrieval problem effectively and is achievable within the \~13-week project timeline[cite: 282, 116]. [cite\_start]It prioritizes doing one thing well—providing accurate answers—before adding more complex features[cite: 283].

-----

## 2\. Target Users

### Primary User Persona

[cite\_start]**User Type:** Incoming and First-Year University Students [cite: 108]

**Demographics:**

  - Age range: 17-19
  - Technical proficiency: High. Comfortable with web and mobile apps, but not developers.
  - Context of use: Primarily on mobile devices while on campus, or on laptops in their dorms.

**User Needs:**

1.  **Need \#1:** To get immediate answers to common campus-related questions.

      - Why it matters: Saves time and reduces the anxiety of not knowing what to do.
      - Current workaround: Asking friends, searching the website for 10-15 minutes, or walking to an office.

2.  **Need \#2:** To trust the information they receive.

      - Why it matters: Official deadlines and policies have significant consequences if misunderstood.
      - Current workaround: Trying to find the official PDF handbook, which can be hard to search.

3.  **Need \#3:** To access information at any time, including outside of office hours.

      - Why it matters: Questions often arise in the evenings or on weekends when offices are closed.
      - Current workaround: Waiting until the next business day, potentially missing a deadline.

**User Pain Points:**

  - Feeling "lost" and not knowing who or where to ask for help.
  - Wasting time searching for information that should be easy to find.
  - Receiving conflicting or outdated advice from different sources.

-----

## 3\. Success Criteria

### Product Success Metrics

[cite\_start]**How we'll know our solution works**[cite: 109]:

1.  **Metric \#1:** Response Quality

      - Target: ≥80% of chatbot answers rated "Helpful" by users via a simple thumbs-up/down button.
      - Measurement method: In-app user feedback buttons logged in the database.

2.  **Metric \#2:** Accuracy

      - Target: Successfully answer ≥85% of questions from a predefined "golden set" of 50 common queries.
      - Measurement method: Internal testing against our evaluation dataset.

3.  **Metric \#3:** User Satisfaction

      - Target: Achieve an average user rating of ≥4 out of 5 stars.
      - Measurement method: A post-interaction pop-up survey.

4.  **Metric \#4:** Engagement

      - Target: Have 20+ unique students use the application during our final user testing phase (Week 14).
      - Measurement method: Basic usage analytics.

5.  **Metric \#5:** Cost Efficiency

      - Target: Keep the average cost per query below $0.05.
      - Measurement method: Monitoring OpenAI API costs and dividing by the number of queries.

-----

### Technical Success Criteria

**Minimum viable performance:**

  - Response latency: \<4 seconds for 95% of queries.
  - Availability: 99% uptime during user testing periods.
  - Error rate: \<2% of API requests result in an error.

-----

### Learning Goals

**What each team member wants to learn:**

**[Team Member 1]:**

  - Implement an end-to-end RAG pipeline using LangChain/LlamaIndex.
  - Build and deploy a scalable backend using FastAPI.

**[Team Member 2]:**

  - Develop a responsive, streaming chat interface with Next.js and React.
  - Learn prompt engineering techniques to improve AI accuracy and prevent misuse.

-----

## 4\. Technical Architecture

### System Overview

Our system is a web application featuring a Next.js frontend that provides a user-friendly chat interface. User queries are sent to a Python FastAPI backend. The backend orchestrates a RAG pipeline, first converting the user's question into an embedding, then searching a PostgreSQL database with the `pgvector` extension to find relevant chunks of text from university documents. These chunks, along with the original question, are sent in a structured prompt to the OpenAI GPT-4o model. The generated answer is then streamed back to the user's interface with citations to the source documents.

### Architecture Diagram

```
┌─────────────┐      ┌─────────────────┐      ┌────────────────┐
│ User        │─────▶│ Frontend        │─────▶│ Backend        │
│ (Browser)   │◀─────│ (Next.js/Vercel)│◀─────│ (FastAPI/Render)│
└─────────────┘      └─────────────────┘      └────────────────┘
                                                      │
                                         ┌────────────┼───────────┐
                                         ▼            ▼           ▼
                               ┌──────────────┐ ┌──────────┐ ┌─────────┐
                               │ OpenAI API   │ │ PostgreSQL │ │ Data    │
                               │ (GPT-4o &    │ │ (pgvector) │ │ Ingestion│
                               │ Embeddings)  │ │            │ │ Script  │
                               └──────────────┘ └──────────┘ └─────────┘
```

-----

### Technology Stack

**Frontend:**

  - Framework: Next.js 14 (React)
  - Key libraries: TailwindCSS, Vercel AI SDK
  - Hosting: Vercel

**Backend:**

  - Framework: FastAPI
  - Language: Python 3.11
  - Hosting: Render

**AI/ML Services:**

  - [cite\_start]Primary model: GPT-4o [cite: 263]
  - Fallback model: GPT-3.5-Turbo
  - Other AI services: OpenAI `text-embedding-3-small` for embeddings

**Data Storage:**

  - Database: PostgreSQL
  - Vector store: `pgvector` extension
  - Object storage: Local storage for initial document processing.

**DevOps/Tooling:**

  - Version control: GitHub
  - CI/CD: GitHub Actions for automated testing and deployment.
  - Testing: `pytest`

-----

### Data Flow

1.  User enters a question in the Next.js frontend.
2.  The frontend sends the query to the `/api/chat` endpoint on the FastAPI backend.
3.  The backend embeds the user's query using `text-embedding-3-small`.
4.  It performs a similarity search against the `pgvector` database to retrieve the top 5 most relevant document chunks.
5.  A prompt is constructed containing the user's query and the retrieved chunks.
6.  The prompt is sent to the GPT-4o model via the OpenAI API.
7.  The AI's response is streamed back to the backend, which in turn streams it to the frontend.
8.  The frontend displays the response to the user, including links to the source documents.

-----

### AI Integration Details

**Retrieval Strategy (if applicable):**

  - Chunking: Recursive character text splitting with a chunk size of 800 tokens and an overlap of 100 tokens.
  - Embedding model: `text-embedding-3-small` for its balance of performance and cost.
  - Similarity metric: Cosine similarity.
  - Top-k: 5 most relevant chunks will be retrieved.

-----

## [cite\_start]5. Risk Assessment [cite: 112]

### Technical Risks

**Risk \#1: Inaccurate AI Responses (Hallucinations)**

  - Likelihood: Medium
  - Impact: High
  - Mitigation:
      - Implement a strong system prompt that strictly instructs the model to answer *only* from the provided context.
      - Always cite the source document, allowing users to verify the information.
      - Regularly evaluate the model's accuracy with our "golden set" of test questions.

### Product Risks

**Risk \#1: Information Becomes Outdated**

  - Likelihood: Medium
  - Impact: High
  - Mitigation:
      - Create a simple process for an administrator to re-ingest new versions of documents (e.g., the new annual student handbook).
      - Display a "Last Updated" timestamp in the UI to inform users of the content's freshness.

### Team Risks

**Risk \#1: Unequal Workload Distribution**

  - Likelihood: Medium
  - Impact: Medium
  - Mitigation:
      - Hold daily stand-ups to track progress and blockers.
      - [cite\_start]Assign clear ownership for each GitHub issue and milestone[cite: 159].

### Safety & Ethical Risks

**Risk \#1: Amplifying Bias from Source Documents**

  - Likelihood: Low
  - Impact: Medium
  - Mitigation:
      - Review source documents for potentially biased or inappropriate content before ingestion.
      - Include a disclaimer in the UI that the chatbot is an AI and may have limitations.

**Risk \#2: Prompt Injection**

  - Likelihood: Medium
  - Impact: High
  - Mitigation:
      - Sanitize user input before it is passed to the backend.
      - Use clear delimiters in the prompt to separate user input from the system instructions.

-----

## [cite\_start]7. User Study Plan [cite: 115]

### Research Ethics

**Do we need IRB approval?**

  - [cite\_start][X] No - but we've completed the IRB Light Checklist (see `docs/irb-checklist.md`) [cite: 57]

**Data we'll collect:**

  - Anonymized chat logs, task completion success rates, and qualitative feedback from surveys.

**User consent:**

  - [X] We've adapted the course consent template for our study.

### Recruitment Plan

**Target participants:**

  - Number: 5-8 first-year KIU students per testing round.
  - Where we'll find them: Flyers in the student center and posts on university-affiliated social media groups.

### Testing Protocol

**Session Structure (30 minutes):**

1.  **Introduction (5 min):** Explain the purpose and get consent.
2.  **Task 1: Find a Deadline (5 min):** "Use the chatbot to find the deadline to withdraw from a class."
3.  **Task 2: Find a Location (5 min):** "Use the chatbot to find the location and hours of the campus health services."
4.  **Task 3: Find a Policy (5 min):** "Use the chatbot to find out the university's policy on plagiarism."
5.  **Post-Task Questions (10 min):** Ask about clarity, usefulness, and overall experience.

-----

## 8\. Project Timeline & Milestones

### Weekly Breakdown

| Week | Focus | Deliverables |
|:---|:---|:---|
| 2 | Planning | [cite\_start]**This proposal**, team contract, repo setup [cite: 3-4] |
| 3 | Backend & UI Setup | "Hello World" FastAPI backend and Next.js chat UI |
| 4 | Design Review | [cite\_start]Updated architecture diagram, initial backlog [cite: 313] |
| 5 | Core RAG Pipeline | [cite\_start]Implement document ingestion, embedding, and retrieval [cite: 146] |
| 6 | End-to-End Flow | Integrate frontend with RAG backend; first AI response |
| 7 | User Testing Round 1 | Test core functionality with 3-5 users |
| 8 | Iteration & Refinement | Implement feedback from user tests |
| 11 | Safety Audit | [cite\_start]Red teaming for harmful responses/prompt injection [cite: 314] |
| 14 | Final Polish & Testing | Final round of user testing, bug fixes |
| 15 | **Final Demo** | [cite\_start]Final presentation, video, and submission [cite: 315] |
