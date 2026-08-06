"""
FILE: app.py

KYA KARTA HAI:
Ye file Streamlit Presentation Layer ki Main Application Coordinator function (`run_app`) ko implement karti hai.

RESPONSIBILITY:
- Master CSS theme inject karna (`inject_styles`)
- Session state initialize karna (`init_session_state`)
- Sidebar render karna (`render_sidebar`)
- Top status bar & Hero render karna (`render_header`)
- Topic Composer card render karna (`render_composer`)
- Agent Pipeline visualizer track render karna (`render_pipeline`)
- Graph run trigger hone par LangGraph stream execution execute karna (`try_stream`), result state update karna, aur auto-activation handle karna
- Active Article Master Workspace render karna (`render_workspace`)

KON USE KARTA HAI:
- Root `app.py` (`streamlit run app.py`)
- `bwa_frontend.py` (backward-compatibility entry point)

DEPENDENCIES:
- streamlit
- os, json
- config/settings -> GOOGLE_API_KEY
- graph/builder -> app (compiled StateGraph)
- graph/runner -> try_stream, extract_latest_state
- utils/markdown -> safe_slug
- persistence/article_store -> extract_title_from_md
- ui/styles -> inject_styles
- ui/state -> init_session_state, add_log
- ui/components/* -> render_sidebar, render_header, render_composer, render_pipeline, render_workspace

REVISION:
app.py = Main Streamlit UI Coordinator.
"""

import json
import os
from typing import Dict, Any

import streamlit as st

from ..config.settings import GOOGLE_API_KEY
from ..graph.builder import app as graph_app
from ..graph.runner import try_stream, extract_latest_state
from ..utils.markdown import safe_slug
from ..persistence.article_store import extract_title_from_md
from .styles import inject_styles
from .state import init_session_state, add_log
from .components import (
    render_header,
    render_sidebar,
    render_composer,
    render_pipeline,
    render_workspace,
)


def run_app():
    """
    Main Streamlit application entry point.
    """
    # 1. Inject Glassmorphism CSS System
    inject_styles()

    # 2. Initialize Session State
    init_session_state()

    # 3. Render Top Status Bar & Hero Banner
    render_header()

    # 4. Render Left Sidebar Controls & Active Article Selector
    as_of = render_sidebar()

    # 5. Render Primary Topic Composer Card
    topic, run_btn = render_composer()

    # 6. Render Agent Pipeline Visualizer Track
    render_pipeline()

    # 7. Execute Graph Stream on Generate Article Button Click
    if run_btn:
        if not topic.strip():
            st.warning("Please enter a topic before generating.")
            st.stop()

        if not os.getenv("GOOGLE_API_KEY", GOOGLE_API_KEY):
            st.error("🔑 `GOOGLE_API_KEY` is missing! Please set your GOOGLE_API_KEY in your `.env` file or environment variables.")
            st.stop()

        inputs: Dict[str, Any] = {
            "topic": topic.strip(),
            "mode": "",
            "needs_research": False,
            "queries": [],
            "evidence": [],
            "plan": None,
            "as_of": as_of.isoformat(),
            "recency_days": 7,
            "sections": [],
            "merged_md": "",
            "md_with_placeholders": "",
            "image_specs": [],
            "final": "",
        }

        status = st.status("Executing Agent Workflow...", expanded=True)
        progress_area = st.empty()

        current_state: Dict[str, Any] = {}
        last_node = None

        for kind, payload in try_stream(graph_app, inputs):
            if kind in ("updates", "values"):
                node_name = None
                if isinstance(payload, dict) and len(payload) == 1 and isinstance(next(iter(payload.values())), dict):
                    node_name = next(iter(payload.keys()))
                if node_name and node_name != last_node:
                    status.write(f"➡️ Node Active: `{node_name}`")
                    st.session_state["current_node"] = node_name
                    last_node = node_name

                current_state = extract_latest_state(current_state, payload)
                summary = {
                    "mode": current_state.get("mode"),
                    "needs_research": current_state.get("needs_research"),
                    "queries": current_state.get("queries", [])[:5] if isinstance(current_state.get("queries"), list) else [],
                    "evidence_count": len(current_state.get("evidence", []) or []),
                    "tasks": len((current_state.get("plan") or {}).get("tasks", [])) if isinstance(current_state.get("plan"), dict) else None,
                    "images": len(current_state.get("image_specs", []) or []),
                    "sections_done": len(current_state.get("sections", []) or []),
                }
                progress_area.json(summary)
                add_log(f"[{kind}] {json.dumps(payload, default=str)[:1200]}")

            elif kind == "final":
                out = payload
                status.update(label="✅ Article Generation Complete", state="complete", expanded=False)
                add_log("[final] received final state")

                # Save generated article & automatically set as Active Article
                plan_obj = out.get("plan")
                if hasattr(plan_obj, "blog_title"):
                    blog_title = plan_obj.blog_title
                elif isinstance(plan_obj, dict):
                    blog_title = plan_obj.get("blog_title", topic.strip())
                else:
                    blog_title = extract_title_from_md(out.get("final", ""), topic.strip())

                art_id = safe_slug(blog_title)
                article_record = {
                    "id": art_id,
                    "title": blog_title,
                    "filename": f"{art_id}.md",
                    "topic": topic.strip(),
                    "plan": out.get("plan"),
                    "evidence": out.get("evidence", []),
                    "image_specs": out.get("image_specs", []),
                    "final": out.get("final", ""),
                    "logs": list(st.session_state.get("logs", [])),
                    "is_historical": False
                }

                st.session_state["articles"][art_id] = article_record
                st.session_state["active_article_id"] = art_id
                st.session_state["last_out"] = article_record

                # Generation complete hone ke baad Article primary output hai,
                # isliye workspace ko automatically Article view par switch karte hain
                # aur pending_article_focus flag set karke single-shot auto-scroll trigger karte hain.
                st.session_state["workspace_view"] = "article"
                st.session_state["pending_article_focus"] = True

                # Progress area ko clear karke rerun karte hain taaki status bar clean ho aur UI Read Mode par transition ho sake.
                progress_area.empty()
                st.rerun()

    # 8. Render Active Article Master Workspace
    render_workspace()


if __name__ == "__main__":
    run_app()


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# User Topic
#     ↓
# Streamlit UI (run_app)
#     ↓
# Graph Runner (try_stream)
#     ↓
# LangGraph (graph/builder.py)
#     ↓
# Router -> Research -> Orchestrator -> Workers -> Reducer -> Images
#     ↓
# Active Article State Setup
#     ↓
# Workspace Render (render_workspace)
#
# Shortcut: run_app() = Master Streamlit application runner.
# ============================================================
