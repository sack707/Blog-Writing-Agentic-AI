"""
FILE: markdown.py

KYA KARTA HAI:
Ye file Markdown manipulation, title slugification, local image resolving, ZIP bundling, aur image fallback card rendering handle karti hai.

RESPONSIBILITY:
- safe_slug(): Titles ko filesystem-safe filenames me convert karna.
- bundle_zip(): Markdown + generated images ko single ZIP file me package karna.
- images_zip(): Images directory ko ZIP package me bundling karna.
- render_markdown_with_local_images(): Markdown article me local image tags aur fallback cards render karna.

KON USE KARTA HAI:
- persistence/article_store.py
- ui/components/article.py
- ui/components/images.py
- agents/image_planner.py

DEPENDENCIES:
- re, zipfile, io.BytesIO, pathlib.Path
- streamlit

REVISION:
markdown.py = Reusable markdown & filesystem packaging utilities.
"""

import re
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Optional, List, Tuple

import streamlit as st


def safe_slug(title: str) -> str:
    """
    Title ko clean filesystem-safe slug string me convert karta hai.
    Example: 'The Modern Python Stack in 2026!' -> 'the_modern_python_stack_in_2026'
    """
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9 _-]+", "", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s or "blog"


def bundle_zip(md_text: str, md_filename: str, images_dir: Path) -> bytes:
    """
    Markdown content aur associated images ko memory ZIP buffer me combine karta hai.
    """
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(md_filename, md_text.encode("utf-8"))

        if images_dir.exists() and images_dir.is_dir():
            for p in images_dir.rglob("*"):
                if p.is_file():
                    z.write(p, arcname=str(p))
    return buf.getvalue()


def images_zip(images_dir: Path) -> Optional[bytes]:
    """
    Images directory ke saare files ko ZIP buffer me convert karta hai.
    """
    if not images_dir.exists() or not images_dir.is_dir():
        return None
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in images_dir.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(p))
    return buf.getvalue()


_MD_IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")
_CAPTION_LINE_RE = re.compile(r"^\*(?P<cap>.+)\*$")
_IMG_FAIL_RE = re.compile(
    r"> \*\*\[IMAGE GENERATION FAILED\]\*\*\s*(?P<caption>.*?)\n>\n> \*\*Alt:\*\*\s*(?P<alt>.*?)\n>\n> \*\*Prompt:\*\*\s*(?P<prompt>.*?)\n>\n> \*\*Error:\*\*\s*(?P<error>.*)",
    re.DOTALL,
)


def _resolve_image_path(src: str) -> Path:
    src = src.strip().lstrip("./")
    return Path(src).resolve()


def render_markdown_with_local_images(md: str):
    """
    Markdown text render karta hai aur local images baseline reference detect karke fallback cards render karta hai.
    """
    if "> **[IMAGE GENERATION FAILED]**" in md:
        def replace_fail_block(m):
            cap = m.group("caption").strip()
            alt = m.group("alt").strip()
            prompt = m.group("prompt").strip()
            err = m.group("error").strip()
            return f"""
<div class="glass-panel image-fallback-card">
    <div class="fallback-header">
        <span class="fallback-icon">🖼️</span>
        <span class="fallback-title">Image Generation Unavailable</span>
    </div>
    <div class="fallback-caption">{cap or alt or 'Technical Diagram Placeholder'}</div>
    <details class="fallback-details">
        <summary>Prompt & Technical Error Details</summary>
        <p><strong>Prompt:</strong> {prompt}</p>
        <p class="fallback-err"><strong>Error:</strong> {err}</p>
    </details>
</div>
"""
        md = _IMG_FAIL_RE.sub(replace_fail_block, md)

    matches = list(_MD_IMG_RE.finditer(md))
    if not matches:
        st.markdown(md, unsafe_allow_html=True)
        return

    parts: List[Tuple[str, str]] = []
    last = 0
    for m in matches:
        before = md[last : m.start()]
        if before:
            parts.append(("md", before))

        alt = (m.group("alt") or "").strip()
        src = (m.group("src") or "").strip()
        parts.append(("img", f"{alt}|||{src}"))
        last = m.end()

    tail = md[last:]
    if tail:
        parts.append(("md", tail))

    i = 0
    while i < len(parts):
        kind, payload = parts[i]

        if kind == "md":
            st.markdown(payload, unsafe_allow_html=True)
            i += 1
            continue

        alt, src = payload.split("|||", 1)

        caption = None
        if i + 1 < len(parts) and parts[i + 1][0] == "md":
            nxt = parts[i + 1][1].lstrip()
            if nxt.strip():
                first_line = nxt.splitlines()[0].strip()
                mcap = _CAPTION_LINE_RE.match(first_line)
                if mcap:
                    caption = mcap.group("cap").strip()
                    rest = "\n".join(nxt.splitlines()[1:])
                    parts[i + 1] = ("md", rest)

        if src.startswith("http://") or src.startswith("https://"):
            st.image(src, caption=caption or (alt or None), use_container_width=True)
        else:
            img_path = _resolve_image_path(src)
            if img_path.exists():
                st.image(str(img_path), caption=caption or (alt or None), use_container_width=True)
            else:
                st.warning(f"Image not found: `{src}` (looked for `{img_path}`)")

        i += 1


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Slug, ZIP packaging, and Markdown rendering helpers.
# Isko call karta hai: ui/components/*, persistence/article_store.py
# Data flow: Title/Markdown -> Helper Functions -> Formatted Output/ZIP
# Shortcut: markdown.py = Formatting & Packaging toolbox.
# ============================================================
