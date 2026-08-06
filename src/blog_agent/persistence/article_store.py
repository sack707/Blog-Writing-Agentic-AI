"""
FILE: article_store.py

KYA KARTA HAI:
Ye file markdown articles ko disk par save karne, list karne, aur read karne ki responsibilities handle karti hai.

RESPONSIBILITY:
- list_past_blogs(): Workspace dir se saare `.md` files scan karke reverse modification time order me return karna.
- read_md_file(): Selected markdown file ko read karke string return karna.
- extract_title_from_md(): Markdown document se `# Title` header parse karna.
- save_article(): Markdown content ko filename slug ke base par disk par write karna.

KON USE KARTA HAI:
- ui/components/sidebar.py
- agents/image_planner.py

DEPENDENCIES:
- pathlib -> Path
- utils/markdown.py -> safe_slug

REVISION:
article_store.py = Local Markdown persistence manager.
"""

from pathlib import Path
from typing import List
from ..utils.markdown import safe_slug
from ..config.settings import ARTICLES_DIR


def list_past_blogs(dir_path: Path = ARTICLES_DIR) -> List[Path]:
    """
    Returns list of `.md` files in directory sorted by modification time (newest first).
    """
    files = [p for p in dir_path.glob("*.md") if p.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def read_md_file(p: Path) -> str:
    """
    Reads markdown file content from path with utf-8 encoding and replace error handler.
    """
    return p.read_text(encoding="utf-8", errors="replace")


def extract_title_from_md(md: str, fallback: str) -> str:
    """
    Parses first `# Title` line from markdown text. Returns fallback if not found.
    """
    for line in md.splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            return t or fallback
    return fallback


def save_article(title: str, md_content: str, dir_path: Path = ARTICLES_DIR) -> Path:
    """
    Saves markdown content to disk as `<slug_title>.md`. Returns destination Path.
    """
    filename = f"{safe_slug(title)}.md"
    out_path = dir_path / filename
    out_path.write_text(md_content, encoding="utf-8")
    return out_path


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Disk persistence for articles (.md files).
# Isko call karta hai: ui/components/sidebar.py, agents/image_planner.py
# Data flow: Markdown String ↔ Disk File
# Shortcut: save_article() / list_past_blogs() = Article Store API.
# ============================================================
