"""
FILE: search.py

KYA KARTA HAI:
Ye file Tavily Web Search API client calls ko isolate karti hai.

RESPONSIBILITY:
Tavily Search API execute karna aur normalized raw dictionary items return karna (url, title, snippet, published_at).

KON USE KARTA HAI:
- agents/researcher.py

DEPENDENCIES:
- langchain_community.tools.tavily_search -> TavilySearchResults
- config/settings.py -> TAVILY_API_KEY

REVISION:
search.py = Web search provider integration.
"""

import os
from typing import List, Dict, Any
from ..config.settings import TAVILY_API_KEY


def tavily_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Executes a web search query via TavilySearchResults and returns raw result dictionaries.
    Returns empty list if TAVILY_API_KEY is missing or if search fails.
    """
    if not os.getenv("TAVILY_API_KEY", TAVILY_API_KEY):
        return []
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults  # type: ignore
        tool = TavilySearchResults(max_results=max_results)
        results = tool.invoke({"query": query})
        out: List[Dict[str, Any]] = []
        for r in results or []:
            out.append(
                {
                    "title": r.get("title") or "",
                    "url": r.get("url") or "",
                    "snippet": r.get("content") or r.get("snippet") or "",
                    "published_at": r.get("published_date") or r.get("published_at"),
                    "source": r.get("source"),
                }
            )
        return out
    except Exception:
        return []


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Tavily web search call execute karna.
# Isko call karta hai: agents/researcher.py
# Data flow: Query string -> tavily_search() -> Raw Dict Results
# Shortcut: tavily_search() = Web research engine provider.
# ============================================================
