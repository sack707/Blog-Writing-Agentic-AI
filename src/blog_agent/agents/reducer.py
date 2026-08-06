"""
FILE: reducer.py

KYA KARTA HAI:
Ye file Reducer Subgraph ka first node (`merge_content`) implement karti hai.

RESPONSIBILITY:
Parallel worker nodes dwara generate kiye gaye Markdown section tuple list `(task_id, section_md)` ko task_id ke order me sort karke full article Markdown (`merged_md`) me combine karna.

KON USE KARTA HAI:
- graph/builder.py (Reducer Subgraph node ke tarah register karne ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState

REVISION:
reducer.py = Consolidates parallel section outputs into one continuous markdown document.
"""

from ..domain.state import BlogState


def merge_content(state: BlogState) -> dict:
    """
    Merge Content Reducer Node:
    - Input: BlogState (sections list containing tuples (task_id, section_md), plan)
    - Action: Sections ko task_id ke order me sort karke # Title ke saath merge karna
    - Output: Dictionary updating merged_md
    """
    plan = state["plan"]
    if plan is None:
        raise ValueError("merge_content called without plan.")

    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]
    body = "\n\n".join(ordered_sections).strip()
    merged_md = f"# {plan.blog_title}\n\n{body}\n"
    return {"merged_md": merged_md}


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Parallel sections ko final document me merge karna.
# Isko call karta hai: graph/builder.py (Reducer Subgraph)
# Data flow: state["sections"] -> merge_content() -> merged_md
# Shortcut: merge_content = Document consolidator node.
# ============================================================
