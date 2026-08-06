"""
FILE: app.py

KYA KARTA HAI:
Ye file project ka main root Streamlit entry point hai (`streamlit run app.py`).

RESPONSIBILITY:
`src/blog_agent/ui/app.py` se `run_app()` call karke BlogAgent application ko launch karna.

KON USE KARTA HAI:
- Developer / User (`streamlit run app.py`)

DEPENDENCIES:
- src.blog_agent.ui.app -> run_app

REVISION:
app.py = Primary application startup script.
"""

import sys
from pathlib import Path

# Add src to sys.path if running as standalone script
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from blog_agent.ui.app import run_app

if __name__ == "__main__":
    run_app()


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# User -> `streamlit run app.py` -> run_app() -> BlogAgent UI
# Shortcut: app.py = Primary entry point.
# ============================================================
