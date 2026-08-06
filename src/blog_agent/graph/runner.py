"""
FILE: runner.py

KYA KARTA HAI:
Ye file Graph execution Helpers (`try_stream` & `extract_latest_state`) ko define karti hai.

RESPONSIBILITY:
- try_stream(): LangGraph compiled app ko stream_mode="updates" me stream karta hai, status steps yield karta hai, aur Gemini quota error (429 / RESOURCE_EXHAUSTED) gracefully handle karta hai.
- extract_latest_state(): Stream updates se dictionary state merge karta hai.

KON USE KARTA HAI:
- ui/app.py
- ui/components/pipeline.py

DEPENDENCIES:
- typing (Dict, Any, Iterator, Tuple)
- streamlit (st.error, st.stop)

REVISION:
runner.py = Graph execution & streaming lifecycle runner.
"""

from typing import Dict, Any, Iterator, Tuple
import streamlit as st


def try_stream(graph_app, inputs: Dict[str, Any]) -> Iterator[Tuple[str, Any]]:
    """
    Streams graph progress steps if available; else invokes graph.
    Yields ("updates"/"values"/"final", payload). Catches rate limit 429 exceptions gracefully.
    """
    try:
        for step in graph_app.stream(inputs, stream_mode="updates"):
            yield ("updates", step)
        out = graph_app.invoke(inputs)
        yield ("final", out)
        return
    except Exception as e:
        err_str = str(e)
        if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
            st.error("⚠️ Gemini API quota exceeded (RESOURCE_EXHAUSTED). Please wait for rate limit reset or check your Google API quota.")
            st.stop()
        raise e


def extract_latest_state(current_state: Dict[str, Any], step_payload: Any) -> Dict[str, Any]:
    """
    Extracts and merges updated state dictionary from stream step payload.
    """
    if isinstance(step_payload, dict):
        if len(step_payload) == 1 and isinstance(next(iter(step_payload.values())), dict):
            inner = next(iter(step_payload.values()))
            current_state.update(inner)
        else:
            current_state.update(step_payload)
    return current_state


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: LangGraph execution stream process karna.
# Isko call karta hai: ui/app.py
# Data flow: Inputs Dict -> try_stream() -> State Updates -> Final Output
# Shortcut: runner.py = Graph execution stream engine.
# ============================================================
