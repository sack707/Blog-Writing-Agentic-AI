"""
FILE: header.py

KYA KARTA HAI:
Ye file Top Status Bar (`Gemini • Connected`) aur Compact Hero Banner (`Research. Plan. Write. Publish.`) ko render karti hai.

RESPONSIBILITY:
- API key connectivity status dot show karna
- Eyebrow tag, gradient header, aur subtitle display karna

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit -> st.markdown
- config/settings -> GOOGLE_API_KEY

REVISION:
header.py = Top navigation status & hero banner component.
"""

import os
import streamlit as st
from ...config.settings import GOOGLE_API_KEY


def render_header():
    """
    Renders Top Status Bar & Compact Hero Banner.
    """
    has_api_key = bool(os.getenv("GOOGLE_API_KEY", GOOGLE_API_KEY))
    status_dot = "status-dot-green" if has_api_key else ""
    status_label = "Gemini • Connected" if has_api_key else "Gemini • Missing Key"

    st.markdown(f"""
    <div class="top-status-bar">
        <div class="status-pill">
            <span class="{status_dot}"></span>
            <span>{status_label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-eyebrow">AGENTIC CONTENT ENGINE</div>
        <div class="hero-main-title">Research. Plan. Write. <span class="gradient-text">Publish.</span></div>
        <div class="hero-sub">Turn an idea into a deeply researched, structured technical article using an autonomous AI workflow.</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Header status pill aur Hero title render karna.
# Isko call karta hai: ui/app.py
# Data flow: render_header() -> HTML Hero Render
# Shortcut: render_header() = Hero & Top Bar component.
# ============================================================
