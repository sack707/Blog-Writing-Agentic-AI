"""
FILE: images.py

KYA KARTA HAI:
Ye file Image Planning Agent ke System Prompt string ko store karti hai.

RESPONSIBILITY:
Merged Markdown me image placeholders (`[[IMAGE_1]]`, etc.) insert karne aur detailed technical diagram prompts propose karne ke rules specify karna.

KON USE KARTA HAI:
- agents/image_planner.py

DEPENDENCIES:
None

REVISION:
images.py = Image placement and prompt planning prompt.
"""

DECIDE_IMAGES_SYSTEM = """You are an expert technical editor.
Decide if images/diagrams are needed for THIS blog.

Rules:
- Max 3 images total.
- Each image must materially improve understanding (diagram/flow/table-like visual).
- Insert placeholders exactly: [[IMAGE_1]], [[IMAGE_2]], [[IMAGE_3]].
- If no images needed: md_with_placeholders must equal input and images=[].
- Avoid decorative images; prefer technical diagrams with short labels.
Return strictly GlobalImagePlan.
"""

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Image planning prompt store karna.
# Isko call karta hai: agents/image_planner.py
# Data flow: Prompt String -> agents/image_planner.py -> Gemini LLM
# Shortcut: DECIDE_IMAGES_SYSTEM = Diagram placement prompt rules.
# ============================================================
