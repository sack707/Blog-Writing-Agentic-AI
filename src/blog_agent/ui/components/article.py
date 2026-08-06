"""
FILE: article.py

KYA KARTA HAI:
Ye file Primary Article Reading Canvas aur Download Action Bar (`⬇️ Download Markdown`, `📦 Download Bundle`) render karti hai.

RESPONSIBILITY:
- Download buttons (Markdown file, ZIP bundle with images) display karna
- Centered 840px reading canvas me Markdown render karna (`render_markdown_with_local_images`)

KON USE KARTA HAI:
- ui/components/workspace.py

DEPENDENCIES:
- streamlit
- pathlib -> Path
- utils/markdown -> safe_slug, bundle_zip, render_markdown_with_local_images
- persistence/article_store -> extract_title_from_md
- config/settings -> IMAGES_DIR

REVISION:
article.py = Main article reading canvas & download toolbar.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st

from ...utils.markdown import safe_slug, bundle_zip, render_markdown_with_local_images
from ...persistence.article_store import extract_title_from_md
from ...config.settings import IMAGES_DIR


def render_article_tab(out: Optional[Dict[str, Any]]):
    """
    Renders Article reading canvas and download action toolbar.
    """
    if not out:
        st.warning("No final article markdown found.")
        return

    final_md = out.get("final") or ""
    if not final_md:
        st.warning("No final article markdown found.")
        return

    blog_title = out.get("title") or extract_title_from_md(final_md, "blog")
    md_filename = out.get("filename") or f"{safe_slug(blog_title)}.md"

    cols_dl = st.columns([1, 1, 4])
    with cols_dl[0]:
        st.download_button(
            "Download Markdown",
            data=final_md.encode("utf-8"),
            file_name=md_filename,
            mime="text/markdown",
            use_container_width=True,
            help="Download article as raw Markdown file (.md)"
        )
    with cols_dl[1]:
        bundle = bundle_zip(final_md, md_filename, IMAGES_DIR)
        st.download_button(
            "Download Bundle",
            data=bundle,
            file_name=f"{safe_slug(blog_title)}_bundle.zip",
            mime="application/zip",
            use_container_width=True,
            help="Download complete ZIP package containing Markdown and generated images"
        )

    # Article canvas directly follows download toolbar without empty container cards
    st.markdown('<div class="article-canvas">', unsafe_allow_html=True)
    render_markdown_with_local_images(final_md)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Article text render aur download toolbar render karna.
# Isko call karta hai: ui/components/workspace.py
# Data flow: out["final"] -> render_article_tab() -> Article Canvas + Download Buttons
# Shortcut: render_article_tab() = Editorial article reader view.
# ============================================================
