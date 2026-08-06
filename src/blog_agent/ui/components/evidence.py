"""
FILE: evidence.py

KYA KARTA HAI:
Ye file Evidence Tab (Research sources, URLs, snippets) render karti hai.

RESPONSIBILITY:
Tavily web research evidence cards display karna ya closed-book / historical notices render karna.

KON USE KARTA HAI:
- ui/components/workspace.py

DEPENDENCIES:
- streamlit

REVISION:
evidence.py = Research citations & evidence tab component.
"""

from typing import Dict, Any, Optional
import streamlit as st


def render_evidence_tab(out: Optional[Dict[str, Any]]):
    """
    Renders Research Evidence tab.
    """
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Research Evidence")
    if not out:
        st.info("No external web evidence required for this topic (Closed-Book mode).")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    evidence = out.get("evidence") or []
    if not evidence:
        if out.get("is_historical"):
            st.info("ℹ️ Research evidence was not persisted for this historical article.")
        else:
            st.info("No external web evidence required for this topic (Closed-Book mode).")
    else:
        for e in evidence:
            if hasattr(e, "model_dump"):
                e = e.model_dump()
            st.markdown(f"""
            <div class="glass-panel" style="margin-bottom: 12px; padding: 16px;">
                <div style="font-weight: 700; color: #f8fafc;">{e.get('title')}</div>
                <div style="font-size: 0.8rem; color: #818cf8; margin: 4px 0;">{e.get('url')}</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">{e.get('snippet') or ''}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Evidence items list render karna.
# Isko call karta hai: ui/components/workspace.py
# Data flow: out["evidence"] -> render_evidence_tab() -> Evidence cards
# Shortcut: render_evidence_tab() = Evidence tab view.
# ============================================================
