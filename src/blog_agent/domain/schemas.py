"""
FILE: schemas.py

KYA KARTA HAI:
Ye file project ke saare Pydantic Data Schemas (Structured Output Models) ko define karti hai.

RESPONSIBILITY:
- Task: Single section writing task specification
- Plan: Complete blog architecture plan
- EvidenceItem: Single web research citation
- EvidencePack: List of evidence items returned by research synthesizer
- RouterDecision: Decision output from Router Agent
- ImageSpec: Single technical diagram specification
- GlobalImagePlan: Complete image placement plan for reducer

KON USE KARTA HAI:
- agents/* (LLM structured output binding ke liye)
- domain/state.py (BlogState me Data Types specify karne ke liye)
- tests/unit/test_utils.py

DEPENDENCIES:
- pydantic (BaseModel, Field)
- typing (List, Optional, Literal)

REVISION:
schemas.py = System ke structured data contracts.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str
    goal: str = Field(..., description="One sentence describing what the reader should do/understand.")
    bullets: List[str] = Field(..., min_length=3, max_length=6)
    target_words: int = Field(..., description="Target words (120–550).")

    tags: List[str] = Field(default_factory=list)
    requires_research: bool = False
    requires_citations: bool = False
    requires_code: bool = False


class Plan(BaseModel):
    blog_title: str
    audience: str
    tone: str
    blog_kind: Literal["explainer", "tutorial", "news_roundup", "comparison", "system_design"] = "explainer"
    constraints: List[str] = Field(default_factory=list)
    tasks: List[Task]


class EvidenceItem(BaseModel):
    title: str
    url: str
    published_at: Optional[str] = None  # ISO "YYYY-MM-DD" preferred
    snippet: Optional[str] = None
    source: Optional[str] = None


class RouterDecision(BaseModel):
    needs_research: bool
    mode: Literal["closed_book", "hybrid", "open_book"]
    reason: str
    queries: List[str] = Field(default_factory=list)
    max_results_per_query: int = Field(5)


class EvidencePack(BaseModel):
    evidence: List[EvidenceItem] = Field(default_factory=list)


class ImageSpec(BaseModel):
    placeholder: str = Field(..., description="e.g. [[IMAGE_1]]")
    filename: str = Field(..., description="Save under images/, e.g. qkv_flow.png")
    alt: str
    caption: str
    prompt: str = Field(..., description="Prompt to send to the image model.")
    size: Literal["1024x1024", "1024x1536", "1536x1024"] = "1024x1024"
    quality: Literal["low", "medium", "high"] = "medium"


class GlobalImagePlan(BaseModel):
    md_with_placeholders: str
    images: List[ImageSpec] = Field(default_factory=list)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Pydantic schemas define karna.
# Isko call karta hai: agents/*, graph/*, domain/state.py
# Data flow: LLM Output -> Pydantic Schema Validation -> Typed Object
# Shortcut: schemas.py = Strict input/output validation contracts.
# ============================================================
