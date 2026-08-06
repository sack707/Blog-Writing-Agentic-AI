"""
FILE: orchestrator.py

KYA KARTA HAI:
Ye file Orchestrator (Planning) Agent ke System Prompt string ko store karti hai.

RESPONSIBILITY:
Topic aur Evidence ke aadhar par structured blog Plan (tasks, word counts, bullets) generate karne ke rules define karna.

KON USE KARTA HAI:
- agents/orchestrator.py

DEPENDENCIES:
None

REVISION:
orchestrator.py = Outline planning prompt.
"""

ORCH_SYSTEM = """You are a senior technical writer and developer advocate.
Produce a highly actionable outline for a technical blog post.

Requirements:
- 5–9 tasks, each with goal + 3–6 bullets + target_words.
- Tags are flexible; do not force a fixed taxonomy.

Grounding:
- closed_book: evergreen, no evidence dependence.
- hybrid: use evidence for up-to-date examples; mark those tasks requires_research=True and requires_citations=True.
- open_book: weekly/news roundup:
  - Set blog_kind="news_roundup"
  - No tutorial content unless requested
  - If evidence is weak, plan should explicitly reflect that (don’t invent events).

Output must match Plan schema.
"""

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Orchestrator planning prompt store karna.
# Isko call karta hai: agents/orchestrator.py
# Data flow: Prompt String -> agents/orchestrator.py -> Gemini LLM
# Shortcut: ORCH_SYSTEM = Outline and task decomposition prompt.
# ============================================================
