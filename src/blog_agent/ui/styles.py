"""
FILE: styles.py

KYA KARTA HAI:
Ye file Streamlit App ke Master CSS Design Tokens aur Glassmorphism Theme Injections ko define karti hai.

RESPONSIBILITY:
- Color tokens, dark background, ambient glows
- Master Content Grid (.block-container max-width 1320px)
- Sidebar, top header status bar, hero banner, composer card styling
- Agent pipeline horizontal track styling
- Article reading canvas, fallback cards, download buttons

KON USE KARTA HAI:
- ui/app.py (inject_styles call ke through)

DEPENDENCIES:
- streamlit -> st.markdown

REVISION:
styles.py = Production Glassmorphism CSS Design System.
"""

import streamlit as st


def inject_styles():
    """
    Injects custom CSS design system into Streamlit frontend.
    """
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-base: #060814;
    --bg-card: rgba(15, 21, 44, 0.65);
    --bg-card-hover: rgba(20, 28, 58, 0.75);
    --border-card: rgba(125, 140, 230, 0.16);
    --border-active: rgba(139, 92, 246, 0.5);
    --accent-purple: #8b5cf6;
    --accent-blue: #3b82f6;
    --accent-indigo: #6366f1;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --radius-main: 16px;
    --radius-sub: 12px;
    --radius-btn: 10px;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
}

/* Master Content Container Alignment */
.block-container {
    max-width: 1320px !important;
    margin: 0 auto !important;
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Base Body Background with Ambient Glows */
.stApp {
    background-color: var(--bg-base) !important;
    background-image: 
        radial-gradient(circle at 75% 12%, rgba(139, 92, 246, 0.15) 0%, transparent 45%),
        radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.10) 0%, transparent 50%) !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit Header Chrome Padding */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
}

/* Master Glass Card System */
.glass-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: var(--radius-main);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

/* Sidebar Styling & Truncation */
section[data-testid="stSidebar"] {
    background-color: rgba(9, 13, 27, 0.95) !important;
    border-right: 1px solid var(--border-card) !important;
    width: 250px !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 16px 0;
}

.brand-icon-main {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #8b5cf6, #3b82f6);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: #ffffff;
    font-size: 1.1rem;
}

.brand-name {
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: -0.02em;
    color: #ffffff;
}

.brand-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: -2px;
}

.nav-item-active {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.25) 0%, rgba(99, 102, 241, 0.15) 100%);
    border: 1px solid rgba(139, 92, 246, 0.4);
    border-radius: 10px;
    color: #ffffff;
    font-weight: 600;
    font-size: 0.88rem;
    margin-bottom: var(--spacing-sm);
}

.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #818cf8;
    margin: 18px 0 10px 0;
}

/* Sidebar Pro Tip Glass Card */
.pro-tip-card {
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: var(--radius-sub);
    padding: 14px;
    margin-top: 20px;
}

.pro-tip-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #c4b5fd;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
}

.pro-tip-desc {
    font-size: 0.76rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* Top Status Bar */
.top-status-bar {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    margin-bottom: var(--spacing-sm);
}

.status-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.78rem;
    font-weight: 500;
    color: #cbd5e1;
    background: rgba(15, 23, 42, 0.7);
    padding: 6px 14px;
    border-radius: 20px;
    border: 1px solid var(--border-card);
}

.status-dot-green {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px rgba(16, 185, 129, 0.8);
}

/* Compact Hero Section */
.hero-wrapper {
    text-align: center;
    max-width: 800px;
    margin: 0 auto var(--spacing-lg) auto;
}

.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 6px;
}

.hero-main-title {
    font-size: clamp(2rem, 2.4vw, 2.6rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 8px;
    color: #ffffff;
}

.gradient-text {
    background: linear-gradient(135deg, #a78bfa 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 0.96rem;
    color: var(--text-secondary);
    font-weight: 400;
    line-height: 1.45;
}

/* Topic Composer Card */
.composer-card {
    background: rgba(13, 18, 38, 0.7);
    border: 1px solid var(--border-card);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-main);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
}

.composer-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: var(--spacing-sm);
}

div[data-baseweb="textarea"] textarea {
    background: rgba(8, 12, 26, 0.8) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-sub) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 14px !important;
}

div[data-baseweb="textarea"] textarea:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.25) !important;
}

/* Generate CTA Button */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--radius-btn) !important;
    height: 44px !important;
    padding: 0 24px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(124, 58, 237, 0.6) !important;
}

/* Pipeline Section Grid Alignment */
.pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--spacing-md);
}

.pipeline-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #ffffff;
}

.pipeline-live {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: #10b981;
    font-weight: 600;
}

.pipeline-track {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 8px;
}

.pipeline-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    text-align: center;
    min-width: 85px;
}

.node-icon-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid var(--border-card);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.88rem;
    color: var(--text-muted);
}

.node-icon-circle.active {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    border-color: #a78bfa;
    color: #ffffff;
    box-shadow: 0 0 16px rgba(139, 92, 246, 0.6);
}

.node-icon-circle.complete {
    background: rgba(16, 185, 129, 0.15);
    border-color: #10b981;
    color: #10b981;
}

.node-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #e2e8f0;
}

.node-desc {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.pipeline-connector-line {
    flex: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.08);
    margin: 0 6px;
    margin-top: -18px;
}

.pipeline-connector-line.complete {
    background: #10b981;
}

/* Workspace Segmented Navigation Control */
div[data-testid="stSegmentedControl"] {
    background: rgba(10, 15, 30, 0.8) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-sub) !important;
    padding: 4px !important;
    gap: 6px !important;
    margin-bottom: var(--spacing-md) !important;
    width: 100% !important;
}

div[data-testid="stSegmentedControl"] button {
    border-radius: 8px !important;
    padding: 8px 18px !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    border: 1px solid transparent !important;
    background: transparent !important;
}

div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background: rgba(139, 92, 246, 0.25) !important;
    color: #ffffff !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(10, 15, 30, 0.8) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: var(--radius-sub) !important;
    padding: 5px !important;
    gap: 6px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 8px 18px !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(139, 92, 246, 0.25) !important;
    color: #ffffff !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
}

/* Plan Rows Cards */
.plan-row-card {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 18px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-sub);
    margin-bottom: 10px;
}

.plan-badge {
    background: rgba(139, 92, 246, 0.2);
    color: #c4b5fd;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 5px 10px;
    border-radius: 6px;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.plan-row-title {
    font-weight: 700;
    font-size: 0.92rem;
    color: #f8fafc;
    margin-bottom: 3px;
}

.plan-row-desc {
    font-size: 0.82rem;
    color: var(--text-secondary);
}

/* Metric Summary Cards */
.metric-box {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border-card);
    border-radius: var(--radius-sub);
    padding: 14px;
    text-align: center;
}

.metric-val {
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffffff;
}

.metric-lbl {
    font-size: 0.76rem;
    color: var(--text-muted);
    margin-top: 2px;
}

/* Article Reading Canvas */
.article-canvas {
    max-width: 880px;
    margin: 0 auto;
    padding: 28px 36px;
    background: rgba(10, 15, 30, 0.6);
    border: 1px solid var(--border-card);
    border-radius: 18px;
    line-height: 1.8;
    font-size: 1rem;
}

.article-canvas h1 { font-size: clamp(32px, 3vw, 44px) !important; font-weight: 800 !important; line-height: 1.18 !important; color: #ffffff !important; margin-bottom: 20px !important; }
.article-canvas h2 { font-size: 1.4rem !important; font-weight: 700 !important; color: #f1f5f9 !important; margin-top: 32px !important; }
.article-canvas code { background: rgba(30, 41, 59, 0.8) !important; color: #38bdf8 !important; padding: 2px 6px !important; border-radius: 6px !important; }
.article-canvas pre { background: #0f172a !important; border: 1px solid var(--border-card) !important; border-radius: 12px !important; padding: 16px !important; }

/* Active Article Header Banner */
.active-article-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: var(--radius-sub);
    margin-bottom: var(--spacing-md);
}

.active-article-title {
    font-weight: 700;
    font-size: 1rem;
    color: #ffffff;
}

.active-article-meta {
    font-size: 0.78rem;
    color: #a5b4fc;
    background: rgba(99, 102, 241, 0.2);
    padding: 4px 12px;
    border-radius: 20px;
}

/* Image Fallback Card */
.image-fallback-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px dashed rgba(245, 158, 11, 0.4);
    border-radius: var(--radius-sub);
    padding: 16px 20px;
    margin: 16px 0;
}
.fallback-header { display: flex; align-items: center; gap: 8px; color: #fbbf24; font-weight: 600; font-size: 0.88rem; }
.fallback-caption { font-size: 0.85rem; color: #cbd5e1; margin: 6px 0; }
.fallback-details { font-size: 0.78rem; color: var(--text-muted); }

/* Download Actions Toolbar Buttons */
div.stDownloadButton > button {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-size: 0.85rem !important;
    height: 38px !important;
    white-space: nowrap !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: var(--spacing-md) !important;
}

div.stDownloadButton > button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Master Glassmorphic CSS Theme Inject karna.
# Isko call karta hai: ui/app.py
# Data flow: inject_styles() -> Streamlit HTML Head Injection -> Formatted UI
# Shortcut: inject_styles() = CSS Design system.
# ============================================================
