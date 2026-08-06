"""
FILE: routing.py

KYA KARTA HAI:
Ye file LangGraph ke Conditional Routing Functions (`route_next` aur `fanout`) ko store karti hai.

RESPONSIBILITY:
- route_next: State se `needs_research` check karke path choose karta hai ("research" vs "orchestrator").
- fanout: Orchestrator ke `Plan.tasks` list me har Task ke liye Send("worker", payload) map karke parallel worker execution enable karta hai.

KON USE KARTA HAI:
- graph/builder.py (add_conditional_edges me specify karne ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState
- langgraph.types -> Send

REVISION:
routing.py = Conditional routing & parallel fanout logic.
"""

from langgraph.types import Send
from ..domain.state import BlogState


def route_next(state: BlogState) -> str:
    """
    Router Conditional Edge:
    - If needs_research is True -> "research" node
    - Else -> "orchestrator" node
    """
    return "research" if state["needs_research"] else "orchestrator"


def fanout(state: BlogState):
    """
    Orchestrator Fanout Conditional Edge:
    - Input: BlogState containing generated Plan object
    - Action: Plan.tasks list ke har Task ke liye Send("worker", task_payload) generate karta hai
    - Output: List of Send objects for parallel section writing
    """
    assert state["plan"] is not None
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["topic"],
                "mode": state["mode"],
                "as_of": state["as_of"],
                "recency_days": state["recency_days"],
                "plan": state["plan"].model_dump(),
                "evidence": [e.model_dump() for e in state.get("evidence", [])],
            },
        )
        for task in state["plan"].tasks
    ]


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: LangGraph graph routing & parallel fanout rules.
# Isko call karta hai: graph/builder.py
# Data flow: BlogState -> route_next() / fanout() -> Target Node / Parallel Sends
# Shortcut: route_next = Switch path | fanout = Parallel worker launcher.
# ============================================================
