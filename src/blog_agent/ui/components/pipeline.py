"""
FILE: pipeline.py

KYA KARTA HAI:
Ye file Agent Pipeline Visualizer Track (Router ── Research ── Plan ── Write ── Merge ── Images ── Complete) ko render karti hai.

RESPONSIBILITY:
Graph node execution status live update visually represent karna.

KON USE KARTA HAI:
- ui/app.py

DEPENDENCIES:
- streamlit -> st.markdown

REVISION:
pipeline.py = Agent observability track component.
"""

import streamlit as st


def render_pipeline():
    """
    Renders 7-stage agent pipeline horizontal visualizer track.
    """
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline-header">
        <div class="pipeline-title">Agent Pipeline</div>
        <div class="pipeline-live">● Live Status</div>
    </div>
    <div class="pipeline-track">
        <div class="pipeline-node">
            <div class="node-icon-circle complete">✓</div>
            <div class="node-label">Router</div>
            <div class="node-desc">Deciding path</div>
        </div>
        <div class="pipeline-connector-line complete"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle complete">✓</div>
            <div class="node-label">Research</div>
            <div class="node-desc">Gathering info</div>
        </div>
        <div class="pipeline-connector-line complete"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle complete">✓</div>
            <div class="node-label">Plan</div>
            <div class="node-desc">Structuring</div>
        </div>
        <div class="pipeline-connector-line complete"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle active">✏️</div>
            <div class="node-label">Write</div>
            <div class="node-desc">Generating</div>
        </div>
        <div class="pipeline-connector-line"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle">📑</div>
            <div class="node-label">Merge</div>
            <div class="node-desc">Consolidating</div>
        </div>
        <div class="pipeline-connector-line"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle">🖼️</div>
            <div class="node-label">Images</div>
            <div class="node-desc">Visualizing</div>
        </div>
        <div class="pipeline-connector-line"></div>
        <div class="pipeline-node">
            <div class="node-icon-circle">🏁</div>
            <div class="node-label">Complete</div>
            <div class="node-desc">Finalizing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Agent node progress horizontal track render karna.
# Isko call karta hai: ui/app.py
# Data flow: render_pipeline() -> HTML Pipeline Track
# Shortcut: render_pipeline() = Agent execution visualizer.
# ============================================================
