"""
FILE: llm.py

KYA KARTA HAI:
Ye file Text LLM (Google Gemini) ke client initialization ko centralize karti hai.

RESPONSIBILITY:
`ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", max_retries=2)` ko single factory function `get_text_llm()` ke through serve karna.

KON USE KARTA HAI:
- agents/router.py
- agents/researcher.py
- agents/orchestrator.py
- agents/writer.py
- agents/image_planner.py

DEPENDENCIES:
- langchain_google_genai -> ChatGoogleGenerativeAI
- config/settings.py -> TEXT_MODEL_NAME, LLM_MAX_RETRIES

REVISION:
llm.py = Centralized LLM factory (Swapping models requires changing only this module).
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from ..config.settings import TEXT_MODEL_NAME, LLM_MAX_RETRIES

# Singleton / Centralized LLM instance
_llm_instance = None


def get_text_llm() -> ChatGoogleGenerativeAI:
    """
    Returns a configured instance of ChatGoogleGenerativeAI.
    Uses model specified in settings (default: gemini-3.5-flash-lite).
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGoogleGenerativeAI(
            model=TEXT_MODEL_NAME,
            max_retries=LLM_MAX_RETRIES
        )
    return _llm_instance


# Export global instance for direct import backwards compatibility
llm = get_text_llm()

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Gemini LLM client return karna.
# Isko call karta hai: agents/*
# Data flow: settings.py -> ChatGoogleGenerativeAI -> Agents
# Shortcut: get_text_llm() = Main reasoning model factory.
# ============================================================
