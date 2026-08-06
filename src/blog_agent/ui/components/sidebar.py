"""
FILE: sidebar.py

KYA KARTA HAI:
Ye file Sidebar Navigation Panel (Brand logo, As-of Date picker, Configuration dropdowns, Saved Articles selector, Pro Tip card) ko render karti hai.

RESPONSIBILITY:
- As-of date picker provide karna
- Saved articles list karke active article switch karna (LOCAL READ, zero API calls)

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit
- datetime.date
- persistence/article_store -> list_past_blogs, read_md_file, extract_title_from_md

REVISION:
sidebar.py = Left navigation and configuration sidebar.
"""

from datetime import date
from pathlib import Path
from typing import Dict, List
import streamlit as st

from ...persistence.article_store import (
    list_past_blogs,
    read_md_file,
    extract_title_from_md,
)


def render_sidebar() -> date:
    """
    Renders left sidebar panel and returns selected as_of date object.
    Handles instant local saved article switching.
    """
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon-main">◈</div>
            <div>
                <div class="brand-name">BlogAgent</div>
                <div class="brand-sub">AI Writing Studio</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-item-active"><span>✦</span> Create Article</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">CONFIGURATION</div>', unsafe_allow_html=True)
        as_of = st.date_input("As-of Date", value=date.today())

        st.selectbox("Research Depth", ["Deep (Recommended)", "Standard", "Fast"], index=0)
        st.selectbox("Sources", ["Web (Default)", "Academic", "News Only"], index=0)
        st.toggle("Image Generation", value=True)

        with st.expander("Advanced Settings"):
            st.caption("Target Words / Section: 350-500")
            st.caption("Max Retries: 2")

        # Saved Articles Selector
        st.markdown('<div class="sidebar-section-title">SAVED ARTICLES</div>', unsafe_allow_html=True)
        past_files = list_past_blogs()

        if not past_files:
            st.caption("No saved articles found in local workspace.")
        else:
            file_by_disp_title: Dict[str, Path] = {}
            options_titles: List[str] = []

            for p in past_files[:40]:
                try:
                    md_text = read_md_file(p)
                    title = extract_title_from_md(md_text, p.stem)
                except Exception:
                    title = p.stem

                disp_title = (title[:28] + "...") if len(title) > 30 else title
                options_titles.append(disp_title)
                file_by_disp_title[disp_title] = p

            curr_active_id = st.session_state.get("active_article_id")
            curr_index = 0
            if curr_active_id:
                for idx, dt in enumerate(options_titles):
                    if file_by_disp_title[dt].stem == curr_active_id:
                        curr_index = idx
                        break

            selected_disp_title = st.selectbox(
                "Select Active Article",
                options=options_titles,
                index=curr_index,
                label_visibility="collapsed"
            )
            selected_file = file_by_disp_title.get(selected_disp_title)

            if selected_file:
                art_id = selected_file.stem
                if art_id != st.session_state.get("active_article_id"):
                    if art_id not in st.session_state["articles"]:
                        md_text = read_md_file(selected_file)
                        art_title = extract_title_from_md(md_text, selected_file.stem)
                        st.session_state["articles"][art_id] = {
                            "id": art_id,
                            "title": art_title,
                            "filename": selected_file.name,
                            "topic": art_title,
                            "plan": None,
                            "evidence": [],
                            "image_specs": [],
                            "final": md_text,
                            "logs": [],
                            "is_historical": True
                        }
                    st.session_state["active_article_id"] = art_id
                    st.session_state["last_out"] = st.session_state["articles"][art_id]

                    # Saved article select karna sirf local navigation operation hai.
                    # Yahan LangGraph/Gemini/Tavily ko kabhi call nahi karna chahiye.
                    # Active article ACTUALLY CHANGE hone par hi workspace_view ko 'article' set karte hain
                    # aur single-shot focus trigger karte hain.
                    st.session_state["workspace_view"] = "article"
                    st.session_state["pending_article_focus"] = True
                    st.rerun()

        st.markdown("""
        <div class="pro-tip-card">
            <div class="pro-tip-title">🚀 Pro Tip</div>
            <div class="pro-tip-desc">Provide specific topics for better research and more focused technical articles.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size: 0.72rem; color: #475569; margin-top: 24px; text-align: center;">
            © 2026 BlogAgent v1.0.0
        </div>
        """, unsafe_allow_html=True)

    return as_of


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Left Sidebar UI & Saved Article Selector.
# Isko call karta hai: ui/app.py
# Ye call karta hai: persistence/article_store.py
# Data flow: Saved .md files -> Sidebar Dropdown -> Active Article State
# Shortcut: render_sidebar() = Sidebar component.
# ============================================================
