"""
FILE: conftest.py

KYA KARTA HAI:
Ye file pytest fixtures and sys.path setup for automated testing define karti hai.

RESPONSIBILITY:
`src` directory ko sys.path me add karna taaki unit tests `blog_agent` package cleanly import kar sakein.

KON USE KARTA HAI:
- pytest runner

DEPENDENCIES:
- sys, pathlib

REVISION:
conftest.py = Pytest configuration and path fixture setup.
"""

import sys
from pathlib import Path

# Add src to sys.path
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
