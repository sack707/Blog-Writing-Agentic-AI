"""
FILE: builder.py

KYA KARTA HAI:
Ye file Complete Multi-Agent LangGraph StateGraph (aur Reducer Subgraph) ko construct aur compile karti hai.

RESPONSIBILITY:
- Reducer Subgraph setup: merge_content -> decide_images -> generate_and_place_images
- Main Graph setup: router -> (research?) -> orchestrator -> worker x N (parallel Send) -> reducer -> END
- Graph compilation: `app = build_graph()`

KON USE KARTA HAI:
- graph/runner.py
- ui/app.py
- bwa_backend.py (backward-compatibility wrapper)
- tests/integration/test_graph_build.py

DEPENDENCIES:
- langgraph.graph -> StateGraph, START, END
- domain/state.py -> BlogState
- agents/* -> router_node, research_node, orchestrator_node, worker_node, merge_content, decide_images, generate_and_place_images
- graph/routing.py -> route_next, fanout

REVISION:
builder.py = Master LangGraph topology architecture.
"""

from langgraph.graph import StateGraph, START, END
from ..domain.state import BlogState
from ..agents.router import router_node
from ..agents.researcher import research_node
from ..agents.orchestrator import orchestrator_node
from ..agents.writer import worker_node
from ..agents.reducer import merge_content
from ..agents.image_planner import decide_images, generate_and_place_images
from .routing import route_next, fanout


def build_reducer_subgraph():
    """
    Builds and compiles the Reducer Subgraph.
    Flow: START -> merge_content -> decide_images -> generate_and_place_images -> END
    """
    reducer_graph = StateGraph(BlogState)
    reducer_graph.add_node("merge_content", merge_content)
    reducer_graph.add_node("decide_images", decide_images)
    reducer_graph.add_node("generate_and_place_images", generate_and_place_images)

    reducer_graph.add_edge(START, "merge_content")
    reducer_graph.add_edge("merge_content", "decide_images")
    reducer_graph.add_edge("decide_images", "generate_and_place_images")
    reducer_graph.add_edge("generate_and_place_images", END)

    return reducer_graph.compile()


def build_graph():
    """
    Builds and compiles the Main BlogAgent StateGraph.
    Topology:
      START
        ↓
      router
        ├── research required ──→ research
        │                            ↓
        └──────────────────────→ orchestrator
                                     ↓
                             Send(worker x N)
                                     ↓
                                  reducer (subgraph)
                                     ↓
                                    END
    """
    reducer_subgraph = build_reducer_subgraph()

    g = StateGraph(BlogState)
    g.add_node("router", router_node)
    g.add_node("research", research_node)
    g.add_node("orchestrator", orchestrator_node)
    g.add_node("worker", worker_node)
    g.add_node("reducer", reducer_subgraph)

    g.add_edge(START, "router")
    g.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
    g.add_edge("research", "orchestrator")

    g.add_conditional_edges("orchestrator", fanout, ["worker"])
    g.add_edge("worker", "reducer")
    g.add_edge("reducer", END)

    return g.compile()


# Global compiled app export
app = build_graph()


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# User Topic
#     ↓
# Streamlit UI (ui/app.py)
#     ↓
# Graph Runner (graph/runner.py)
#     ↓
# Router (agents/router.py)
#     ├── research required ──→ Researcher (agents/researcher.py)
#     │                           ↓
#     └──────────────────────→ Orchestrator (agents/orchestrator.py)
#                                 ↓
#                               Plan
#                                 ↓
#                         Send(worker × N) (agents/writer.py)
#                                 ↓
#                          Draft Sections
#                                 ↓
#                              Reducer (agents/reducer.py)
#                                 ↓
#                           Image Planner (agents/image_planner.py)
#                                 ↓
#                           Final Article
#                                 ↓
#                            Persistence (persistence/article_store.py)
#                                 ↓
#                          Streamlit Workspace (ui/components/*)
#
# Yaad rakhne ka shortcut:
# builder.py = Master graph topology blueprint.
# ============================================================
