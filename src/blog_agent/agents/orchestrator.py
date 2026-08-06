"""
FILE: orchestrator.py

KYA KARTA HAI:
Ye file Orchestrator (Planning) Agent Node ko implement karti hai.

RESPONSIBILITY:
User topic, mode, aur gathered Evidence ke aadhar par complete Structured `Plan` (5-9 sections/tasks with goals, bullets, and target words) generate karna.

KON USE KARTA HAI:
- graph/builder.py (Orchestrator Node ke tarah register karne ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState
- domain/schemas.py -> Plan
- providers/llm.py -> get_text_llm
- prompts/orchestrator.py -> ORCH_SYSTEM

REVISION:
orchestrator.py = Master planner node that creates section task breakdown.
"""

from langchain_core.messages import SystemMessage, HumanMessage

from ..domain.state import BlogState
from ..domain.schemas import Plan
from ..providers.llm import get_text_llm
from ..prompts.orchestrator import ORCH_SYSTEM


def orchestrator_node(state: BlogState) -> dict:
    """
    Orchestrator Agent Node:
    - Input: BlogState (topic, mode, evidence, as_of date)
    - Action: Gemini se structured Plan (tasks list) generate karwana
    - Output: Dictionary updating plan object
    """
    llm = get_text_llm()
    planner = llm.with_structured_output(Plan)
    mode = state.get("mode", "closed_book")
    evidence = state.get("evidence", [])

    forced_kind = "news_roundup" if mode == "open_book" else None

    plan = planner.invoke(
        [
            SystemMessage(content=ORCH_SYSTEM),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n"
                    f"Mode: {mode}\n"
                    f"As-of: {state['as_of']} (recency_days={state['recency_days']})\n"
                    f"{'Force blog_kind=news_roundup' if forced_kind else ''}\n\n"
                    f"Evidence:\n{[e.model_dump() for e in evidence][:16]}"
                )
            ),
        ]
    )
    if forced_kind:
        plan.blog_kind = "news_roundup"

    return {"plan": plan}


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Article ka complete section plan banana.
# Isko call karta hai: graph/builder.py
# Ye call karta hai: providers/llm.py (Gemini structured output Plan)
# Data flow: Topic + Evidence -> orchestrator_node() -> Plan Object
# Shortcut: orchestrator_node = Master outline architect.
# ============================================================
