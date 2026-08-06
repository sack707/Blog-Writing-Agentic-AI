"""
FILE: researcher.py

KYA KARTA HAI:
Ye file Research Agent Node implement karti hai.

RESPONSIBILITY:
- Router queries par Tavily web search run karna
- Search results ko Gemini se synthesize karke clean `EvidenceItem` objects me convert karna
- Recency filters (e.g. open_book 7 days) apply karna

KON USE KARTA HAI:
- graph/builder.py (Research Node ke tarah register karne ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState
- domain/schemas.py -> EvidencePack, EvidenceItem
- providers/llm.py -> get_text_llm
- providers/search.py -> tavily_search
- prompts/research.py -> RESEARCH_SYSTEM

REVISION:
researcher.py = Web search aggregator & evidence synthesizer node.
"""

from datetime import date, timedelta
from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage

from ..domain.state import BlogState
from ..domain.schemas import EvidencePack, EvidenceItem
from ..providers.llm import get_text_llm
from ..providers.search import tavily_search
from ..prompts.research import RESEARCH_SYSTEM


def _iso_to_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    try:
        return date.fromisoformat(s[:10])
    except Exception:
        return None


def research_node(state: BlogState) -> dict:
    """
    Research Agent Node:
    - Input: BlogState (queries, as_of date, recency_days, mode)
    - Action: Tavily web search runs -> Gemini structures raw results -> Deduplication & recency filter
    - Output: Dictionary updating evidence list
    """
    queries = (state.get("queries") or [])[:10]
    raw: List[dict] = []
    for q in queries:
        raw.extend(tavily_search(q, max_results=6))

    if not raw:
        return {"evidence": []}

    llm = get_text_llm()
    extractor = llm.with_structured_output(EvidencePack)
    pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(
                content=(
                    f"As-of date: {state['as_of']}\n"
                    f"Recency days: {state['recency_days']}\n\n"
                    f"Raw results:\n{raw}"
                )
            ),
        ]
    )

    dedup = {}
    for e in pack.evidence:
        if e.url:
            dedup[e.url] = e
    evidence = list(dedup.values())

    if state.get("mode") == "open_book":
        as_of = date.fromisoformat(state["as_of"])
        cutoff = as_of - timedelta(days=int(state["recency_days"]))
        evidence = [e for e in evidence if (d := _iso_to_date(e.published_at)) and d >= cutoff]

    return {"evidence": evidence}


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Web evidence gather aur clean karna.
# Isko call karta hai: graph/builder.py
# Ye call karta hai: providers/search.py (Tavily), providers/llm.py (Gemini)
# Data flow: Queries -> tavily_search() -> EvidencePack -> evidence list
# Shortcut: research_node = Web evidence synthesizer.
# ============================================================
