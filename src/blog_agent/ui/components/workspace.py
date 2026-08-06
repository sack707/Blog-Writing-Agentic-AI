"""
FILE: workspace.py

KYA KARTA HAI:
Ye file Active Article Master Workspace container, stable anchor, single-shot auto-scroll trigger, aur state-driven workspace navigation (`📋 Plan`, `🔍 Evidence`, `📝 Article`, `🖼️ Images`, `📜 Agent Logs`) render karti hai.

RESPONSIBILITY:
- Stable element anchor (`<div id="article-workspace"></div>`) render karna
- Post-generation ya saved article selection par single-shot iframe-isolated auto-scroll execute karna
- Active article header banner show karna
- State-controlled segmented navigation toolbar (`render_workspace_navigation`) render karna
- Active view according to `st.session_state["workspace_view"]` render karna

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit
- streamlit.components.v1
- ui/components/plan -> render_plan_tab
- ui/components/evidence -> render_evidence_tab
- ui/components/article -> render_article_tab
- ui/components/images -> render_images_tab
- ui/components/logs -> render_logs_tab

REVISION:
workspace.py = Master state-controlled workspace & auto-focus controller.
"""

from typing import Dict, Any, Optional
import streamlit as st
import streamlit.components.v1 as components

from .plan import render_plan_tab
from .evidence import render_evidence_tab
from .article import render_article_tab
from .images import render_images_tab
from .logs import render_logs_tab


def render_workspace():
    """
    Renders Active Article Master Workspace and manages state-driven tab routing.
    """
    # 1. Stable custom element anchor for viewport scroll target
    st.markdown('<div id="article-workspace"></div>', unsafe_allow_html=True)

    # 2. Single-shot auto-scroll execution (iframe-isolated parent document window scroll)
    # Ye flag sirf ek baar article par focus karne ke liye use hota hai.
    # Normal Streamlit rerun me isko consume karke False set kar dete hain,
    # taaki page download button click ya setting change par dobara scroll na kare.
    if st.session_state.get("pending_article_focus"):
        components.html(
            """
            <script>
            try {
                const el = window.parent.document.getElementById('article-workspace');
                if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            } catch (e) {
                console.error('Auto-scroll error:', e);
            }
            </script>
            """,
            height=0,
        )
        st.session_state["pending_article_focus"] = False

    active_art_id = st.session_state.get("active_article_id")
    out: Optional[Dict[str, Any]] = (
        st.session_state["articles"].get(active_art_id)
        if active_art_id
        else st.session_state.get("last_out")
    )

    # 3. Render Active Article Banner if article payload exists
    if out:
        art_title = out.get("title") or (
            out.get("plan").blog_title if hasattr(out.get("plan"), "blog_title") else "Active Article Workspace"
        )
        is_historical = out.get("is_historical", False)
        meta_tag = "Saved • Historical Markdown" if is_historical else "Active • Full Agent Output"

        st.markdown(f"""
        <div class="active-article-banner">
            <div class="active-article-title">📖 {art_title}</div>
            <div class="active-article-meta">{meta_tag}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4. State-controlled Segmented Navigation Toolbar
    view_options = ["📋 Plan", "🔍 Evidence", "📝 Article", "🖼️ Images", "📜 Agent Logs"]
    view_map = {
        "📋 Plan": "plan",
        "🔍 Evidence": "evidence",
        "📝 Article": "article",
        "🖼️ Images": "images",
        "📜 Agent Logs": "logs"
    }
    key_map = {v: k for k, v in view_map.items()}

    current_view_key = st.session_state.get("workspace_view", "article" if out else "plan")
    current_label = key_map.get(current_view_key, "📝 Article" if out else "📋 Plan")

    # Keep widget state in sync with workspace_view
    if st.session_state.get("workspace_nav_control") != current_label:
        st.session_state["workspace_nav_control"] = current_label

    selected_label = st.segmented_control(
        "Workspace Navigation",
        options=view_options,
        default=current_label,
        key="workspace_nav_control",
        label_visibility="collapsed"
    )

    if selected_label and view_map.get(selected_label) != current_view_key:
        st.session_state["workspace_view"] = view_map[selected_label]
        st.rerun()

    # 5. Render Active View Content
    active_view = st.session_state.get("workspace_view", "article" if out else "plan")

    if out:
        if active_view == "plan":
            render_plan_tab(out)
        elif active_view == "evidence":
            render_evidence_tab(out)
        elif active_view == "article":
            render_article_tab(out)
        elif active_view == "images":
            render_images_tab(out)
        elif active_view == "logs":
            render_logs_tab(out)
        else:
            render_article_tab(out)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; color: var(--text-muted);" class="glass-panel">
            <h3 style="color: #f8fafc; font-weight: 700; margin-bottom: 8px;">No Article Selected</h3>
            <p style="font-size: 0.9rem;">Generate a new article above or select an existing one from Saved Articles in the sidebar.</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Article workspace container, anchor, auto-scroll, & state navigation.
# Isko call karta hai: ui/app.py
# Ye call karta hai: ui/components/{plan, evidence, article, images, logs}.py
# Data flow: Active Article Payload + workspace_view -> workspace.py -> Selected View
# Shortcut: render_workspace() = State-controlled workspace view.
# ============================================================

