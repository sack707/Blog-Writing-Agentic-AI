"""
FILE: research.py

KYA KARTA HAI:
Ye file Research Synthesizer Agent ke System Prompt string ko store karti hai.

RESPONSIBILITY:
Raw Tavily search results se high-quality EvidenceItem objects synthesize aur deduplicate karne ke rules define karna.

KON USE KARTA HAI:
- agents/researcher.py

DEPENDENCIES:
None

REVISION:
research.py = Web search evidence extraction prompt.
"""

RESEARCH_SYSTEM = """You are a research synthesizer.

Given raw web search results, produce EvidenceItem objects.

Rules:
- Only include items with a non-empty url.
- Prefer relevant + authoritative sources.
- Normalize published_at to ISO YYYY-MM-DD if reliably inferable; else null (do NOT guess).
- Keep snippets short.
- Deduplicate by URL.
"""

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Research prompt store karna.
# Isko call karta hai: agents/researcher.py
# Data flow: Prompt String -> agents/researcher.py -> Gemini LLM
# Shortcut: RESEARCH_SYSTEM = Search result extraction prompt.
# ============================================================
