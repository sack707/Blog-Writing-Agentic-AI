# Universal Agent Development Framework

This document outlines a **Universal Mental Model** for designing and implementing ANY Production AI Agent System.

---

## The 5-Layer Mental Model: T-M-A-O-O

When building any agent, avoid choosing an LLM or framework first. Follow the **T-M-A-O-O Framework**:

1. **THINK (Problem & Contract)**: What problem are we solving? What enters and leaves the system?
2. **MODEL (State & Schemas)**: What data must persist between steps? What outputs must be strictly structured?
3. **ACT (Tools, Prompts, & Nodes)**: What capabilities does the LLM lack? What individual agent nodes exist?
4. **ORCHESTRATE (Routing & Graph)**: Which decisions control the next step? How are nodes wired into a StateGraph?
5. **OPERATE (Persistence, Observability, UI, & Testing)**: How is state saved? How is progress visualised? How are nodes tested without wasting API quota?

---

## English Version: 15-Step Universal Flow

### Step 1 — Problem Definition
- Clearly describe the agent's objective.

### Step 2 — Input / Output Contract
- **Input**: User topic, target audience, recency dates.
- **Output**: Formatted Markdown document, citations, visual diagrams.

### Step 3 — Define Shared State
- Identify all variables that must survive between node transitions (e.g. `queries`, `evidence`, `plan`, `sections`).

### Step 4 — Define Pydantic Schemas
- Enforce strict typing for critical decisions (e.g. `RouterDecision`, `Plan`, `GlobalImagePlan`).

### Step 5 — Identify Tools
- Equip the agent with capabilities LLMs lack natively (e.g. Tavily search tool, image generator).

### Step 6 — Design Agent Nodes
- Break the problem into single-responsibility nodes (`router`, `researcher`, `orchestrator`, `writer`, `reducer`, `image_planner`).

### Step 7 — Write Focused Prompts
- Give each node a single, explicit system prompt.

### Step 8 — Define Routing Logic
- Write conditional edges (e.g. `needs_research -> research OR orchestrator`).

### Step 9 — Build the Graph
- Wire nodes and edges using a framework like LangGraph (`StateGraph`).

### Step 10 — Create Runner Entry Point
- Provide a clean runner (`try_stream`) to invoke or stream graph progress.

### Step 11 — Persistence Layer
- Save outputs to local disk (`.md` files) or database.

### Step 12 — Observability & Error Handling
- Log step execution; catch rate limits (429) gracefully.

### Step 13 — User Interface
- Expose controls via CLI, REST API, or Streamlit dashboard.

### Step 14 — Testing Strategy
- Write unit tests for schemas/utils; test graph topology without calling live LLM APIs.

### Step 15 — Deployment & Configuration
- Isolate environment settings (`.env`, `settings.py`).

---

## Hinglish Version: Universal Agent Learning Guide

### Agent Banane Ka Secret Mental Model

Agent banane se pehle LLM choose mat karo. Sabse pehle in questions ke answers dhoondho:

1. **PROBLEM & CONTRACT**:
   - *Agent ka actual kaam kya hai?*
   - *User input me kya dega aur final output me kya chahiye?*

2. **STATE**:
   - *Beech ke execution steps me information ko yaad kaise rakhenge?*
   - Wahi tumhara `BlogState` hai.

3. **SCHEMAS**:
   - *Kaunsi information strict JSON format me chahiye?*
   - Uske liye Pydantic `BaseModel` schemas banao (`Plan`, `RouterDecision`).

4. **TOOLS**:
   - *LLM khud se web search ya image generate nahi kar sakta.*
   - Uske liye Tavily aur Gemini Image API tools chahiye.

5. **NODES / AGENTS**:
   - *Problem ko independent responsibilities me kaise todein?*
   - Router -> Researcher -> Orchestrator -> Writer -> Reducer.

6. **ROUTING & GRAPH**:
   - *Kaunsa node kab chalega?*
   - LangGraph `StateGraph` me nodes aur conditional edges connect karo.

7. **PERSISTENCE & UI**:
   - *Final output save kahan hoga aur user ko dikhega kaise?*
   - Local `.md` files + Streamlit Glassmorphism UI.

---

## Mapping Framework to BlogAgent

| Universal Step | BlogAgent Implementation |
| :--- | :--- |
| **Problem** | Researched technical blog post generation |
| **Contract** | Input: `topic` + `as_of` \| Output: `final` Markdown + Images |
| **State** | `src/blog_agent/domain/state.py` (`BlogState`) |
| **Schemas** | `src/blog_agent/domain/schemas.py` (`Plan`, `Task`, `RouterDecision`) |
| **Tools** | `src/blog_agent/providers/search.py` & `image.py` |
| **Nodes** | `src/blog_agent/agents/` (`router`, `researcher`, `orchestrator`, `writer`, `reducer`, `image_planner`) |
| **Routing** | `src/blog_agent/graph/routing.py` (`route_next`, `fanout`) |
| **Graph** | `src/blog_agent/graph/builder.py` (`StateGraph`) |
| **Persistence** | `src/blog_agent/persistence/article_store.py` |
| **Interface** | `src/blog_agent/ui/app.py` (Streamlit Studio) |
| **Testing** | `tests/unit/test_utils.py` & `tests/integration/test_graph_build.py` |
