"""
FILE: image_planner.py

KYA KARTA HAI:
Ye file Image Planning (`decide_images`) aur Image Generation (`generate_and_place_images`) Agent Nodes ko implement karti hai.

RESPONSIBILITY:
- decide_images: Merged markdown me technical diagram placeholders (`[[IMAGE_1]]`) insert karna aur Structured `GlobalImagePlan` generate karna.
- generate_and_place_images: Propose kiye gaye diagram prompts ko Gemini Image API par send karna, images under `images/` save karna, markdown placeholders ko image tags se replace karna, aur gracefully fallback card inject karna agar error aaye.

KON USE KARTA HAI:
- graph/builder.py (Reducer Subgraph me register hone ke liye)

DEPENDENCIES:
- domain/state.py -> BlogState
- domain/schemas.py -> GlobalImagePlan
- providers/llm.py -> get_text_llm
- providers/image.py -> gemini_generate_image_bytes
- prompts/images.py -> DECIDE_IMAGES_SYSTEM
- utils/markdown.py -> safe_slug

REVISION:
image_planner.py = Visual diagram planning and image injection nodes.
"""

from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage

from ..domain.state import BlogState
from ..domain.schemas import GlobalImagePlan
from ..providers.llm import get_text_llm
from ..providers.image import gemini_generate_image_bytes
from ..prompts.images import DECIDE_IMAGES_SYSTEM
from ..utils.markdown import safe_slug
from ..config.settings import IMAGES_DIR, ARTICLES_DIR


def decide_images(state: BlogState) -> dict:
    """
    Decide Images Node:
    - Input: BlogState (merged_md, topic, plan)
    - Action: Gemini Structured Output se diagram prompts & placeholders generate karna
    - Output: Dictionary updating md_with_placeholders & image_specs
    """
    llm = get_text_llm()
    planner = llm.with_structured_output(GlobalImagePlan)
    merged_md = state["merged_md"]
    plan = state["plan"]
    assert plan is not None

    image_plan = planner.invoke(
        [
            SystemMessage(content=DECIDE_IMAGES_SYSTEM),
            HumanMessage(
                content=(
                    f"Blog kind: {plan.blog_kind}\n"
                    f"Topic: {state['topic']}\n\n"
                    "Insert placeholders + propose image prompts.\n\n"
                    f"{merged_md}"
                )
            ),
        ]
    )

    return {
        "md_with_placeholders": image_plan.md_with_placeholders,
        "image_specs": [img.model_dump() for img in image_plan.images],
    }


def generate_and_place_images(state: BlogState) -> dict:
    """
    Generate & Place Images Node:
    - Input: BlogState (md_with_placeholders, merged_md, image_specs, plan)
    - Action: Gemini image model invoke karna, disk par image PNGs save karna, placeholders replace karna, markdown article disk par write karna
    - Output: Dictionary updating final Markdown content
    """
    plan = state["plan"]
    assert plan is not None

    md = state.get("md_with_placeholders") or state["merged_md"]
    image_specs = state.get("image_specs", []) or []

    # If no images requested, write merged markdown to disk
    if not image_specs:
        filename = f"{safe_slug(plan.blog_title)}.md"
        out_path = ARTICLES_DIR / filename
        out_path.write_text(md, encoding="utf-8")
        return {"final": md}

    images_dir = IMAGES_DIR
    images_dir.mkdir(exist_ok=True)

    for spec in image_specs:
        placeholder = spec["placeholder"]
        filename = spec["filename"]
        out_path = images_dir / filename

        if not out_path.exists():
            try:
                img_bytes = gemini_generate_image_bytes(spec["prompt"])
                out_path.write_bytes(img_bytes)
            except Exception as e:
                # Graceful fallback card formatting
                prompt_block = (
                    f"> **[IMAGE GENERATION FAILED]** {spec.get('caption','')}\n>\n"
                    f"> **Alt:** {spec.get('alt','')}\n>\n"
                    f"> **Prompt:** {spec.get('prompt','')}\n>\n"
                    f"> **Error:** {e}\n"
                )
                md = md.replace(placeholder, prompt_block)
                continue

        img_md = f"![{spec['alt']}](images/{filename})\n*{spec['caption']}*"
        md = md.replace(placeholder, img_md)

    filename = f"{safe_slug(plan.blog_title)}.md"
    out_path = ARTICLES_DIR / filename
    out_path.write_text(md, encoding="utf-8")
    return {"final": md}


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Images plan karna aur generate karke place karna.
# Isko call karta hai: graph/builder.py (Reducer Subgraph)
# Ye call karta hai: providers/image.py (Gemini Image API), utils/markdown.py
# Data flow: merged_md -> decide_images() -> generate_and_place_images() -> final
# Shortcut: decide_images / generate_and_place_images = Image pipeline nodes.
# ============================================================
