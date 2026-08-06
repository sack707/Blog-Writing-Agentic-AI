"""
FILE: logs.py

KYA KARTA HAI:
Ye file Agent Logs Tab (Developer Console monospaced execution logs text area) render karti hai.

RESPONSIBILITY:
Graph node stream steps aur execution logs output render karna.

KON USE KARTA HAI:
- ui/components/workspace.py

DEPENDENCIES:
- streamlit

REVISION:
logs.py = Developer execution console tab.
"""

from typing import Dict, Any, Optional
import streamlit as st


def render_logs_tab(out: Optional[Dict[str, Any]]):
    """
    Renders Developer Execution Console tab.
    """
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Developer Execution Logs")

    log_list = (out.get("logs") if out else None) or st.session_state.get("logs", [])
    if not log_list and out and out.get("is_historical"):
        st.info("ℹ️ Agent execution logs are unavailable for this historical saved article.")
    else:
        st.text_area("Console Output", value="\n\n".join(log_list[-80:]), height=480)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Developer execution logs console render karna.
# Isko call karta hai: ui/components/workspace.py
# Data flow: st.session_state["logs"] -> render_logs_tab() -> Text Area Console
# Shortcut: render_logs_tab() = Developer console view.
# ============================================================
