"""
FILE: router.py

KYA KARTA HAI:
Ye file Router Agent ki logic implement karti hai.

RESPONSIBILITY:
User topic ko evaluate karke Structured Output `RouterDecision` generate karna (closed_book, hybrid, open_book) aur recency_days set karna.

KON USE KARTA HAI:
- graph/builder.py (Router Node ke tarah register karne ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState
- domain/schemas.py -> RouterDecision
- providers/llm.py -> get_text_llm
- prompts/router.py -> ROUTER_SYSTEM
- langchain_core.messages -> SystemMessage, HumanMessage

REVISION:
router.py = First decision node in LangGraph flow.
"""

from langchain_core.messages import SystemMessage, HumanMessage
from ..domain.state import BlogState
from ..domain.schemas import RouterDecision
from ..providers.llm import get_text_llm
from ..prompts.router import ROUTER_SYSTEM


def router_node(state: BlogState) -> dict:
    """
    Router Agent Node:
    - Input: BlogState (topic, as_of date)
    - Action: Gemini se routing decision leta hai
    - Output: Dictionary updating needs_research, mode, queries, recency_days
    """
    llm = get_text_llm()
    decider = llm.with_structured_output(RouterDecision)
    decision = decider.invoke(
        [
            SystemMessage(content=ROUTER_SYSTEM),
            HumanMessage(content=f"Topic: {state['topic']}\nAs-of date: {state['as_of']}"),
        ]
    )

    if decision.mode == "open_book":
        recency_days = 7
    elif decision.mode == "hybrid":
        recency_days = 45
    else:
        recency_days = 3650

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days,
    }


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Topic ki research requirement decide karna.
# Isko call karta hai: graph/builder.py (Node in StateGraph)
# Ye call karta hai: providers/llm.py (Gemini structured output)
# Data flow: BlogState (topic, as_of) -> router_node() -> State Update (needs_research, queries)
# Shortcut: router_node = Traffic controller node.
# ============================================================
