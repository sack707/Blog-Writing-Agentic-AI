"""
FILE: plan.py

KYA KARTA HAI:
Ye file Plan Tab (2-column layout: Left 70% section rows, Right 30% 2x2 metric cards summary) ko render karti hai.

RESPONSIBILITY:
- Plan tasks render karna (numbered badges `01`, `02`...)
- Sections, Est. Words, Sources, Est. Read Time, Article Focus summary metrics render karna

KON USE KARTA HAI:
- ui/components/workspace.py

DEPENDENCIES:
- streamlit
- json

REVISION:
plan.py = 2-column Plan tab component.
"""

import json
from typing import Dict, Any, Optional
import streamlit as st


def render_plan_tab(out: Optional[Dict[str, Any]]):
    """
    Renders 2-column Plan dashboard tab.
    """
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    if not out:
        st.info("ℹ️ Plan data was not persisted for this historical article.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    plan_obj = out.get("plan")
    if not plan_obj:
        st.info("ℹ️ Plan data was not persisted for this historical article.")
    else:
        if hasattr(plan_obj, "model_dump"):
            plan_dict = plan_obj.model_dump()
        elif isinstance(plan_obj, dict):
            plan_dict = plan_obj
        else:
            plan_dict = json.loads(json.dumps(plan_obj, default=str))

        tasks = plan_dict.get("tasks", [])
        task_count = len(tasks)

        col_plan_left, col_plan_right = st.columns([7, 3])

        with col_plan_left:
            st.markdown(f"### Article Plan <span style='font-size: 0.8rem; background: rgba(139,92,246,0.2); color: #c4b5fd; padding: 4px 10px; border-radius: 12px;'>{task_count} Sections</span>", unsafe_allow_html=True)
            for t in tasks:
                t_id = f"{t.get('id'):02d}"
                t_title = t.get("title", "")
                t_goal = t.get("goal", "")
                st.markdown(f"""
                <div class="plan-row-card">
                    <div class="plan-badge">{t_id}</div>
                    <div>
                        <div class="plan-row-title">{t_title}</div>
                        <div class="plan-row-desc">{t_goal}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_plan_right:
            st.markdown("### Plan Summary")
            mcol1, mcol2 = st.columns(2)
            with mcol1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{task_count}</div>
                    <div class="metric-lbl">Sections</div>
                </div>
                """, unsafe_allow_html=True)
            with mcol2:
                total_words = sum(t.get("target_words", 0) for t in tasks)
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{total_words}+</div>
                    <div class="metric-lbl">Est. Words</div>
                </div>
                """, unsafe_allow_html=True)

            mcol3, mcol4 = st.columns(2)
            with mcol3:
                ev_count = len(out.get("evidence", []) or [])
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{ev_count if ev_count > 0 else 'N/A'}</div>
                    <div class="metric-lbl">Sources</div>
                </div>
                """, unsafe_allow_html=True)
            with mcol4:
                est_mins = max(5, round(total_words / 200))
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-val">{est_mins} min</div>
                    <div class="metric-lbl">Est. Read Time</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-top: 16px;" class="glass-panel">
                <div style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600;">Article Focus</div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #a5b4fc; margin-top: 4px;">Technical Deep Dive</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Plan tab dashboard view render karna.
# Isko call karta hai: ui/components/workspace.py
# Data flow: out["plan"] -> render_plan_tab() -> Section rows + Metrics
# Shortcut: render_plan_tab() = Plan dashboard view.
# ============================================================
