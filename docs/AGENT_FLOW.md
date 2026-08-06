# LangGraph Agent Execution Lifecycle

## Overview
This document explains the step-by-step lifecycle of a request inside the BlogAgent **LangGraph StateGraph**.

---

## Complete Request Sequence

```
User Topic Input (Streamlit)
          ↓
     ui/app.py
          ↓
    graph/runner.py (try_stream)
          ↓
┌─────────────────────────────────────────────────────────────┐
│ LANGGRAPH STATEGRAPH EXECUTION                              │
│                                                             │
│ 1. router_node (agents/router.py)                           │
│    - Evaluates topic & as_of date                           │
│    - Mode: closed_book | hybrid | open_book                 │
│                                                             │
│ 2. route_next (graph/routing.py)                            │
│    ├── needs_research == True ──→ research_node            │
│    │                              (agents/researcher.py)    │
│    │                                    ↓                   │
│    └───────────────────────────→ orchestrator_node          │
│                                   (agents/orchestrator.py)  │
│                                         ↓                   │
│ 3. fanout (graph/routing.py)                                │
│    - Maps Plan.tasks to Send("worker", task_payload)       │
│                                         ↓                   │
│ 4. worker_node x N (agents/writer.py) [PARALLEL]            │
│    - Generates markdown section for assigned task           │
│    - Appends (task.id, section_md) to state                 │
│                                         ↓                   │
│ 5. reducer_subgraph (graph/builder.py)                      │
│    a) merge_content (agents/reducer.py)                     │
│       - Sorts sections by task_id and joins into merged_md  │
│    b) decide_images (agents/image_planner.py)               │
│       - Proposes GlobalImagePlan with [[IMAGE_N]] tags      │
│    c) generate_and_place_images (agents/image_planner.py)   │
│       - Invokes Gemini Image API, saves PNGs to images/,    │
│         writes final .md to disk, handles fallbacks         │
└─────────────────────────────────────────────────────────────┘
          ↓
  Active Article Session State Updated
          ↓
   Streamlit Workspace Renders Final Tabs
```

---

## State Transformation Map

| Graph Step | Input State Fields | Output State Fields |
| :--- | :--- | :--- |
| `router` | `topic`, `as_of` | `needs_research`, `mode`, `queries`, `recency_days` |
| `research` | `queries`, `as_of`, `recency_days`, `mode` | `evidence` (list of `EvidenceItem`) |
| `orchestrator` | `topic`, `mode`, `evidence`, `as_of` | `plan` (`Plan` object with `tasks` list) |
| `worker` (x N) | `task`, `topic`, `mode`, `plan`, `evidence` | `sections` (accumulated list of `(id, section_md)`) |
| `merge_content` | `sections`, `plan` | `merged_md` |
| `decide_images` | `merged_md`, `topic`, `plan` | `md_with_placeholders`, `image_specs` |
| `generate_and_place_images` | `md_with_placeholders`, `image_specs`, `plan` | `final` (writes `<slug>.md` file to disk) |
