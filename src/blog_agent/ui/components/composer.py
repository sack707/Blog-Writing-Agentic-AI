"""
FILE: composer.py

KYA KARTA HAI:
Ye file Topic Composer Surface (Textarea, example triggers, `Generate Article →` button) ko render karti hai.

RESPONSIBILITY:
- Topic textarea input accept karna
- `💡 Try example` aur `📝 Load saved` preset buttons handle karna
- Primary `Generate Article →` button trigger expose karna

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit
- persistence/article_store -> list_past_blogs, read_md_file, extract_title_from_md

REVISION:
composer.py = Main input card surface component.
"""

from typing import Tuple
import streamlit as st
from ...persistence.article_store import list_past_blogs, read_md_file, extract_title_from_md


def render_composer() -> Tuple[str, bool]:
    """
    Renders Topic Composer card.
    Returns tuple: (topic_text, is_generate_clicked)
    """
    st.markdown('<div class="composer-card">', unsafe_allow_html=True)
    st.markdown('<div class="composer-title">What do you want to write about?</div>', unsafe_allow_html=True)

    topic_prefill_val = st.session_state.get("topic_prefill", "")
    topic = st.text_area(
        "Topic Input",
        value=topic_prefill_val if isinstance(topic_prefill_val, str) else "",
        placeholder="e.g. The future of Python free-threading and GIL removal in 2026...",
        height=85,
        label_visibility="collapsed"
    )

    cols_comp = st.columns([1, 1, 2])
    with cols_comp[0]:
        if st.button("💡 Try example", use_container_width=True):
            st.session_state["topic_prefill"] = "The future of Python free-threading and GIL removal in 2026"
            st.rerun()
    with cols_comp[1]:
        if st.button("📝 Load saved", use_container_width=True):
            past_files = list_past_blogs()
            if past_files:
                md_text = read_md_file(past_files[0])
                title = extract_title_from_md(md_text, past_files[0].stem)
                st.session_state["topic_prefill"] = title
                st.rerun()

    with cols_comp[2]:
        run_btn = st.button("Generate Article →", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return topic, run_btn


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: User topic input capture karna.
# Isko call karta hai: ui/app.py
# Data flow: User input -> (topic, run_btn) -> ui/app.py -> Graph Execution
# Shortcut: render_composer() = Topic input card component.
# ============================================================
