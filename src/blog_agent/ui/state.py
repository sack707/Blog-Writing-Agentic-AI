"""
FILE: state.py

KYA KARTA HAI:
Ye file Streamlit Session State keys (`articles`, `active_article_id`, `last_out`, `logs`, `topic_prefill`) ki clean, centralized initialization handle karti hai.

RESPONSIBILITY:
Streamlit reruns par duplicated `if key not in st.session_state` initializations ko avoid karna.

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit -> st.session_state

REVISION:
state.py = Centralized Streamlit session state manager.
"""

import streamlit as st


def init_session_state():
    """
    Initializes required session state keys if not present.
    """
    if "articles" not in st.session_state:
        st.session_state["articles"] = {}

    if "active_article_id" not in st.session_state:
        st.session_state["active_article_id"] = None

    if "last_out" not in st.session_state:
        st.session_state["last_out"] = None

    if "logs" not in st.session_state:
        st.session_state["logs"] = []

    if "topic_prefill" not in st.session_state:
        st.session_state["topic_prefill"] = ""

    # Workspace view: Default 'plan' agar naye session me active article nahi hai,
    # otherwise default to 'article' for reading mode.
    if "workspace_view" not in st.session_state:
        st.session_state["workspace_view"] = "article" if st.session_state.get("active_article_id") else "plan"

    # Ye flag sirf ek baar article par auto-scroll focus karne ke liye use hota hai.
    # Normal Streamlit rerun me isko dobara True nahi karna hai,
    # warna page baar-baar article section par jump karega.
    if "pending_article_focus" not in st.session_state:
        st.session_state["pending_article_focus"] = False


def add_log(msg: str):
    """
    Appends a log message string to session state logs.
    """
    if "logs" not in st.session_state:
        st.session_state["logs"] = []
    st.session_state["logs"].append(msg)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Streamlit session_state keys initialize karna.
# Isko call karta hai: ui/app.py
# Data flow: init_session_state() -> st.session_state populated
# Shortcut: init_session_state() = UI state setup.
# ============================================================

