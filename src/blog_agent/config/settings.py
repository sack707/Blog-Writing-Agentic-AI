"""
FILE: settings.py

KYA KARTA HAI:
Ye file project ke centralized configuration aur environment variables ko manage karti hai.

RESPONSIBILITY:
- Environment variables (.env) load karna
- LLM model names (Gemini 3.5 Flash Lite) set karna
- Tavily Search & Gemini Image API keys configure karna
- Default paths (articles, images) define karna

KON USE KARTA HAI:
- providers/llm.py (Gemini text model ke liye)
- providers/search.py (Tavily search ke liye)
- providers/image.py (Gemini image model ke liye)
- persistence/article_store.py (Paths ke liye)

DEPENDENCIES:
- dotenv -> load_dotenv
- os -> os.getenv

REVISION:
Config Layer = Pure settings, zero business logic.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Environment variables load karte hain
load_dotenv()

# LLM Configuration
TEXT_MODEL_NAME = os.getenv("TEXT_MODEL_NAME", "gemini-3.5-flash-lite")
IMAGE_MODEL_NAME = os.getenv("IMAGE_MODEL_NAME", "gemini-2.5-flash-image")
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "2"))

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMAGES_DIR = BASE_DIR / "images"
ARTICLES_DIR = BASE_DIR

# Default Recency Settings
DEFAULT_RECENCY_DAYS_OPEN_BOOK = 7
DEFAULT_RECENCY_DAYS_HYBRID = 45
DEFAULT_RECENCY_DAYS_CLOSED_BOOK = 3650

# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: Project ke settings & API keys store karna.
# Isko call karta hai: providers/*, persistence/*, agents/*
# Data flow: .env file -> settings.py -> Provider & Service modules
# Shortcut: settings.py = Single source of truth for config.
# ============================================================
