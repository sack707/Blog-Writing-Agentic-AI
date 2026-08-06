"""
FILE: test_utils.py

KYA KARTA HAI:
Ye file utility functions (`_message_text`, `safe_slug`, Pydantic Schemas) ke unit tests run karti hai without calling external APIs.

RESPONSIBILITY:
- _message_text handling strings vs Gemini lists
- safe_slug slugification
- Task, Plan, RouterDecision schema instantiation

KON USE KARTA HAI:
- pytest runner / manual validation

DEPENDENCIES:
- blog_agent.utils -> _message_text, safe_slug
- blog_agent.domain -> Task, Plan, RouterDecision

REVISION:
test_utils.py = Zero-API unit test suite.
"""

import sys
from pathlib import Path

src_path = Path(__file__).resolve().parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from blog_agent.utils.messages import _message_text
from blog_agent.utils.markdown import safe_slug
from blog_agent.domain.schemas import Task, Plan, RouterDecision


def test_message_text_string():
    assert _message_text("hello world") == "hello world"
    assert _message_text(None) == ""


def test_message_text_list():
    gemini_block = [{"type": "text", "text": "generated section markdown"}]
    assert _message_text(gemini_block) == "generated section markdown"


def test_safe_slug():
    assert safe_slug("The Modern Python Stack in 2026!") == "the_modern_python_stack_in_2026"
    assert safe_slug("   Free-Threading GIL Removal   ") == "free-threading_gil_removal"


def test_schemas():
    task = Task(id=1, title="Intro", goal="Goal", bullets=["b1", "b2", "b3"], target_words=200)
    assert task.id == 1
    assert task.target_words == 200

    plan = Plan(blog_title="Test Title", audience="Developers", tone="Technical", tasks=[task])
    assert plan.blog_title == "Test Title"

    decision = RouterDecision(needs_research=True, mode="hybrid", reason="Needs examples", queries=["q1"])
    assert decision.needs_research is True
    assert decision.mode == "hybrid"


if __name__ == "__main__":
    test_message_text_string()
    test_message_text_list()
    test_safe_slug()
    test_schemas()
    print("All unit tests passed successfully!")
