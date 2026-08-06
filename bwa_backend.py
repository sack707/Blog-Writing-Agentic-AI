"""
FILE: bwa_backend.py

KYA KARTA HAI:
Ye file backward-compatibility wrapper hai jo modularized `src/blog_agent` package se compiled graph (`app`) aur schemas re-export karti hai.

RESPONSIBILITY:
Purane code / scripts jo `from bwa_backend import app` import karte hain unhe break na karna.

KON USE KARTA HAI:
- Legacy scripts / unit tests

DEPENDENCIES:
- src.blog_agent.graph.builder -> app
- src.blog_agent.domain -> Plan, Task, EvidenceItem, RouterDecision, EvidencePack, ImageSpec, GlobalImagePlan, BlogState

REVISION:
bwa_backend.py = Backward compatibility wrapper.
"""

import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from blog_agent.graph.builder import app, build_graph
from blog_agent.domain import (
    Task,
    Plan,
    EvidenceItem,
    RouterDecision,
    EvidencePack,
    ImageSpec,
    GlobalImagePlan,
    BlogState,
)
from blog_agent.providers import get_text_llm, llm

# Backward compatibility alias
State = BlogState

__all__ = [
    "app",
    "build_graph",
    "Task",
    "Plan",
    "EvidenceItem",
    "RouterDecision",
    "EvidencePack",
    "ImageSpec",
    "GlobalImagePlan",
    "BlogState",
    "State",
    "get_text_llm",
    "llm",
]


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Legacy imports to new modular architecture mapping.
# Isko call karta hai: External scripts / Legacy imports
# Ye re-export karta hai: src/blog_agent/graph/builder.py -> app
# Shortcut: bwa_backend.py = Compatibility bridge.
# ============================================================
