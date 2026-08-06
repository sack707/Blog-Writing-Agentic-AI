"""
FILE: router.py

KYA KARTA HAI:
Ye file Router Agent ke System Prompt string ko store karti hai.

RESPONSIBILITY:
User topic ko assess karne ke liye LLM guidance rules define karna (closed_book, hybrid, open_book).

KON USE KARTA HAI:
- agents/router.py

DEPENDENCIES:
None

REVISION:
router.py = Traffic controller prompt.
"""

ROUTER_SYSTEM = """You are a routing module for a technical blog planner.

Decide whether web research is needed BEFORE planning.

Modes:
- closed_book (needs_research=false): evergreen concepts.
- hybrid (needs_research=true): evergreen + needs up-to-date examples/tools/models.
- open_book (needs_research=true): volatile weekly/news/"latest"/pricing/policy.

If needs_research=true:
- Output 3–10 high-signal, scoped queries.
- For open_book weekly roundup, include queries reflecting last 7 days.
"""

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Router prompt store karna.
# Isko call karta hai: agents/router.py
# Data flow: Prompt String -> agents/router.py -> Gemini LLM
# Shortcut: ROUTER_SYSTEM = Research requirement prompt rules.
# ============================================================
