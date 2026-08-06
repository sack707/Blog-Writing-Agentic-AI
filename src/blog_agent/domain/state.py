"""
FILE: state.py

KYA KARTA HAI:
Ye file LangGraph StateGraph ka central shared memory state (`BlogState` TypedDict) define karti hai.

RESPONSIBILITY:
Graph execution ke har step me kaunsa data store hoga aur nodes ke beech pass hoga usko specify karna.
`sections` field me `operator.add` reducer function use hoti hai taaki parallel worker nodes ke section outputs append ho sakein.

KON USE KARTA HAI:
- agents/* (Har node BlogState receive karta hai aur updated state dict return karta hai)
- graph/builder.py (StateGraph(BlogState) instantiate karne ke liye)

DEPENDENCIES:
- typing (TypedDict, List, Optional, Annotated)
- operator (add reducer for list concatenation)
- domain/schemas.py (EvidenceItem, Plan)

REVISION:
state.py = LangGraph flow ki shared memory blackboard.
"""

import operator
from typing import TypedDict, List, Optional, Annotated
from .schemas import EvidenceItem, Plan


class BlogState(TypedDict):
    topic: str

    # routing / research
    mode: str
    needs_research: bool
    queries: List[str]
    evidence: List[EvidenceItem]
    plan: Optional[Plan]

    # recency
    as_of: str
    recency_days: int

    # workers reducer (parallel worker outputs accumulate in this list)
    sections: Annotated[List[tuple[int, str]], operator.add]  # (task_id, section_md)

    # reducer/image
    merged_md: str
    md_with_placeholders: str
    image_specs: List[dict]

    final: str


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: LangGraph state schema define karna.
# Isko call karta hai: agents/*, graph/builder.py
# Data flow: User Topic -> BlogState -> Node updates -> Final State
# Shortcut: BlogState = Shared graph blackboard.
# ============================================================
