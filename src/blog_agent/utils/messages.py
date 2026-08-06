"""
FILE: messages.py

KYA KARTA HAI:
Ye file LangChain / Gemini ke AIMessage object se safely plain text extract karti hai.

RESPONSIBILITY:
Gemini model string content ke bajaye multi-block lists `[{'type': 'text', 'text': '...'}]` return kar sakta hai.
Ye helper function use clean string me normalize karta hai taaki AttributeError na aaye.

KON USE KARTA HAI:
- agents/writer.py (worker_node response parsing ke waqt)
- tests/unit/test_utils.py

DEPENDENCIES:
- Standard Python types (str, list, dict)

REVISION:
messages.py = Robust AIMessage content extractor.
"""

from typing import Any


def _message_text(message: Any) -> str:
    """
    Safely extract plain text from an AIMessage or raw content value.
    Handles both plain string content and Gemini multi-block list structures:
    - "hello" -> "hello"
    - [{"type": "text", "text": "hello"}] -> "hello"
    """
    if message is None:
        return ""

    content = getattr(message, "content", message)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, str):
                texts.append(part)
            elif isinstance(part, dict):
                if part.get("type") == "text" and "text" in part:
                    texts.append(str(part["text"]))
                elif "text" in part and part.get("type") != "non_text" and part.get("type") != "image_url":
                    texts.append(str(part["text"]))
        return "\n".join(texts)

    return str(content) if content is not None else ""


# ============================================================
# REVISION / CONNECTION MAP
# ============================================================
# Is file ka main kaam: LLM AIMessage se plain text extract karna.
# Isko call karta hai: agents/writer.py
# Data flow: AIMessage -> _message_text() -> Clean Markdown String
# Shortcut: _message_text = Multi-block safe text parser.
# ============================================================
