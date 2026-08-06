"""
Ye package BlogAgent ke system prompts ko expose karta hai.
"""
from .router import ROUTER_SYSTEM
from .research import RESEARCH_SYSTEM
from .orchestrator import ORCH_SYSTEM
from .writer import WORKER_SYSTEM
from .images import DECIDE_IMAGES_SYSTEM

__all__ = [
    "ROUTER_SYSTEM",
    "RESEARCH_SYSTEM",
    "ORCH_SYSTEM",
    "WORKER_SYSTEM",
    "DECIDE_IMAGES_SYSTEM",
]
