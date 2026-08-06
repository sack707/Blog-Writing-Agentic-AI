# ◈ BlogAgent — Autonomous AI Blog Writing Platform

BlogAgent is a production-grade, multi-agent AI system built using **LangGraph**, **Google Gemini 3.5 Flash Lite**, **Tavily Web Search**, and **Streamlit**.

It transforms a high-level user prompt into a deeply researched, structured, and visually illustrated technical blog post.

---

## Key Features

- **Autonomous Agent Routing**: Dynamically decides whether web research is needed (`closed_book`, `hybrid`, or `open_book`).
- **Web Evidence Gathering**: Synthesizes real-time web search results using Tavily Search API.
- **Hierarchical Outline Planning**: Decomposes topics into structured section tasks with word count budgets and citation rules.
- **Parallel Fan-out Section Writing**: Uses LangGraph `Send` API to generate all blog sections concurrently.
- **Technical Diagram Generation**: Proposes visual placeholders and generates inline technical diagrams using Gemini's image API (`gemini-2.5-flash-image`).
- **Dark Glassmorphism Studio UI**: Features a 2026 AI SaaS interface with active article state management, pipeline observability, and local article downloads (Markdown / ZIP bundle).

---

## Tech Stack

- **Agent Framework**: LangGraph (`StateGraph`, `Send` fan-out, conditional routing)
- **LLM Provider**: Google Gemini (`gemini-3.5-flash-lite` text model, `gemini-2.5-flash-image` image model)
- **Web Search**: Tavily Search API (`langchain_community.tools.tavily_search`)
- **Frontend Framework**: Streamlit
- **Data Validation**: Pydantic v2
- **Language**: Python 3.10+

---

## Quick Setup & Running Locally

### 1. Clone & Setup Environment
```bash
git clone https://github.com/campusx-official/blog-writing-agent.git
cd blog-writing-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## Project Structure & Map

```
blog-writing-agent/
├── app.py                      # Main entry point (`streamlit run app.py`)
├── bwa_backend.py              # Backward-compatibility export wrapper
├── bwa_frontend.py             # Backward-compatibility export wrapper
│
├── src/blog_agent/
│   ├── config/settings.py      # Config & env variables
│   ├── domain/
│   │   ├── schemas.py          # Pydantic data schemas (Plan, Task, RouterDecision)
│   │   └── state.py            # LangGraph shared memory state (BlogState)
│   ├── prompts/                # Isolated prompt templates (router, research, orchestrator, writer, images)
│   ├── providers/              # External API adapters (Gemini text/image LLM, Tavily search)
│   ├── agents/                 # Agent node implementations (router, researcher, orchestrator, writer, reducer, image_planner)
│   ├── graph/                  # LangGraph topology builder, routing edges, and execution runner
│   ├── persistence/            # Disk storage for .md articles
│   ├── utils/                  # Reusable text, markdown, and packaging helpers
│   └── ui/                     # Modular Streamlit components & glassmorphism theme
│
├── tests/
│   ├── unit/                   # Zero-API unit tests
│   └── integration/            # Graph compilation & topology tests
│
└── docs/                       # Architectural & learning guides
```

### Project File Map

| File | Purpose | Called By | Calls | Important Data |
| :--- | :--- | :--- | :--- | :--- |
| `config/settings.py` | Centralized settings & API keys | `providers/*` | `os.getenv` | API keys, Model IDs |
| `domain/schemas.py` | Pydantic data contracts | `agents/*`, `domain/state.py` | `pydantic` | `Plan`, `Task`, `RouterDecision` |
| `domain/state.py` | LangGraph shared memory | `graph/*`, `agents/*` | `domain/schemas.py` | `BlogState` |
| `providers/llm.py` | Gemini LLM client factory | `agents/*` | `langchain_google_genai` | `ChatGoogleGenerativeAI` |
| `providers/search.py` | Tavily web search wrapper | `agents/researcher.py` | `TavilySearchResults` | Raw Search Results |
| `providers/image.py` | Gemini Image generation | `agents/image_planner.py` | `google-genai` | Raw Image Bytes |
| `graph/builder.py` | Compiles StateGraph topology | `ui/app.py`, `graph/runner.py` | `agents/*`, `graph/routing.py` | Compiled `app` |
| `ui/app.py` | Main Streamlit coordinator | `app.py` | `ui/components/*`, `graph/runner.py` | User Session State |

---

## Agent Workflow Lifecycle

```
User Topic Input
     ↓
  Router Agent (Decides closed_book / hybrid / open_book)
     ├── Needs Research ──→ Researcher Agent (Tavily search -> Evidence Pack)
     │                           ↓
     └─────────────────→ Orchestrator Agent (Creates multi-task Plan)
                                 ↓
                         Send Fan-Out (Parallel Workers x N)
                                 ↓
                         Reducer Subgraph (Merges sections -> Proposes Image Plan -> Generates Diagrams)
                                 ↓
                         Final Markdown Article & Workspace UI
```

---

## Running Automated Tests

Run tests without consuming API quota:
```bash
python tests/unit/test_utils.py
python tests/integration/test_graph_build.py
```

---

## Interview Guide (30s, 2min, 5min Explanations)

### 30-Second Elevator Pitch
> "I built an autonomous multi-agent blog writing platform using LangGraph and Google Gemini. It analyzes user topics, dynamically searches the web for evidence when needed, creates an architectural outline, fan-outs section writing across parallel worker nodes, generates technical diagrams, and renders the result in a modern Streamlit AI studio."

### 2-Minute System Summary
> "The architecture follows clean software engineering principles with strict layer boundaries. `domain/` contains Pydantic models like `Plan` and `Task`. `providers/` isolates LLM and Search APIs. The agent workflow starts with a `Router Node` that decides research requirements. If required, the `Researcher Node` queries Tavily and synthesizes citations. The `Orchestrator Node` plans section tasks, which are executed concurrently using LangGraph's `Send` fanout. Finally, a `Reducer Subgraph` merges sections and generates technical diagrams via Gemini's multimodal API."

### 5-Minute Technical Deep Dive
> See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/AGENT_FLOW.md](docs/AGENT_FLOW.md) for full request lifecycle diagrams.

---

## Documentation Links

- [Architecture & Layer Boundaries](docs/ARCHITECTURE.md)
- [LangGraph Execution Lifecycle](docs/AGENT_FLOW.md)
- [Developer Guide (Adding Agents, Tools, Providers)](docs/DEVELOPER_GUIDE.md)
- [Universal Agent Development Framework (English & Hinglish)](docs/HOW_TO_BUILD_ANY_AGENT.md)
